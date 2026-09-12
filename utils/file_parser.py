"""Universal document extraction with scanned-PDF detection and optional OCR."""
from __future__ import annotations
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
import fitz
from docx import Document

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}

@dataclass
class ExtractionResult:
    text: str
    pages: int = 0
    ocr_pages: int = 0
    tables: int = 0
    mode: str = "text"


def _ocr_page(page) -> str:
    """OCR one rendered page using RapidOCR when available.

    OCR is imported lazily so a normal text-PDF deployment does not fail if the
    optional OCR runtime is unavailable. The caller receives a clear error only
    when OCR is actually needed.
    """
    try:
        from rapidocr_onnxruntime import RapidOCR
    except Exception as exc:
        raise RuntimeError(
            "This PDF appears to be scanned/image-based, but the OCR engine could not be loaded. "
            "Please confirm rapidocr-onnxruntime is installed or upload a text-based PDF."
        ) from exc
    pix = page.get_pixmap(matrix=fitz.Matrix(1.6, 1.6), alpha=False)
    image_bytes = pix.tobytes("png")
    result, _ = RapidOCR()(image_bytes)
    if not result:
        return ""
    lines = []
    for item in result:
        try:
            lines.append(str(item[1]))
        except Exception:
            continue
    return "\n".join(lines)


def extract_document(file_name: str, data: bytes) -> ExtractionResult:
    ext = Path(file_name).suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {ext or 'unknown'}")
    if not data:
        raise ValueError("The uploaded file is empty.")

    if ext == ".pdf":
        doc = fitz.open(stream=data, filetype="pdf")
        try:
            page_texts = [page.get_text("text").strip() for page in doc]
            pages = len(doc)
            ocr_pages = 0
            parts = []
            for i, raw in enumerate(page_texts):
                # A page with almost no text but visible content is treated as a scan.
                if len(raw.strip()) < 40:
                    ocr = _ocr_page(doc[i]).strip()
                    if ocr:
                        parts.append(f"[Page {i+1}]\n{ocr}")
                        ocr_pages += 1
                    elif raw:
                        parts.append(f"[Page {i+1}]\n{raw}")
                else:
                    if raw:
                        parts.append(f"[Page {i+1}]\n{raw}")
            text = "\n\n".join(parts).strip()
            mode = "ocr+text" if ocr_pages and any(page_texts) else ("ocr" if ocr_pages else "text")
            if not text:
                # Some scanned pages do not expose an image list reliably; OCR all pages as a last resort.
                for i, page in enumerate(doc):
                    ocr = _ocr_page(page).strip()
                    if ocr:
                        parts.append(f"[Page {i+1}]\n{ocr}")
                        ocr_pages += 1
                text = "\n\n".join(parts).strip()
                mode = "ocr"
            if not text:
                raise ValueError(f"No readable text could be extracted from '{file_name}'.")
            return ExtractionResult(text=text, pages=pages, ocr_pages=ocr_pages, mode=mode)
        finally:
            doc.close()

    if ext == ".docx":
        doc = Document(BytesIO(data))
        parts = [p.text for p in doc.paragraphs if p.text.strip()]
        table_count = 0
        for table in doc.tables:
            table_count += 1
            for row in table.rows:
                parts.append(" | ".join(cell.text.strip() for cell in row.cells))
        text = "\n".join(parts).strip()
        if not text:
            raise ValueError(f"No extractable text was found in '{file_name}'.")
        return ExtractionResult(text=text, pages=1, tables=table_count, mode="text")

    text = data.decode("utf-8-sig", errors="replace").strip()
    if not text:
        raise ValueError(f"No extractable text was found in '{file_name}'.")
    return ExtractionResult(text=text, pages=1, mode="text")


def extract_text(file_name: str, data: bytes) -> str:
    return extract_document(file_name, data).text
