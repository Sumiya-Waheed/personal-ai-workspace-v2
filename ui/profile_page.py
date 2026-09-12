import streamlit as st
from utils.validators import validate_upload
from ui.theme import hero, metric


def render(state):
    hero("CAREER", "My Profile", "Create one verified personal knowledge base from your CV, projects, certificates, achievements and experience.")
    uploads = st.file_uploader("Profile documents", type=["pdf","docx","txt"], accept_multiple_files=True, key="profile_uploader", help="Text PDFs, scanned PDFs, DOCX and TXT are supported. Scanned PDFs can use OCR when needed.")
    if uploads:
        bad = []
        for f in uploads:
            ok, msg = validate_upload(f.name, f.size)
            if not ok: bad.append(msg)
        if bad:
            for msg in bad: st.error(msg)
        elif st.button("Build verified knowledge base", type="primary", use_container_width=True):
            with st.spinner("Extracting, OCR-checking, chunking and indexing your documents…"):
                try:
                    docs = state["profile_manager"].rebuild(uploads)
                    state["profile_docs"] = docs
                    state["profile_files"] = [f.name for f in uploads]
                    state["match_result"] = None
                    st.success(f"Knowledge base ready: {len(docs)} document(s), {len(state['profile_manager'].store.records)} evidence chunks.")
                except Exception as exc:
                    st.error(str(exc))
    cols = st.columns(3)
    with cols[0]: metric("Documents", str(len(state.get("profile_docs", []))))
    with cols[1]: metric("Evidence chunks", str(len(state.get("profile_manager").store.records) if state.get("profile_manager") else 0))
    with cols[2]: metric("Processing", "Ready" if state.get("profile_docs") else "Waiting")
    if state.get("profile_docs"):
        st.markdown("<div class='section-label'>Sources in your profile</div>", unsafe_allow_html=True)
        for doc in state["profile_docs"]:
            st.markdown(f"<div class='card'><h3>📄 {doc.filename}</h3><p>{doc.document_type} · {doc.pages} page(s) · {doc.chunks} chunks · OCR pages: {doc.ocr_pages} · {doc.mode}</p></div>", unsafe_allow_html=True)
