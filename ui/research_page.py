import streamlit as st
from research.assistant import ResearchAssistant
from ui.theme import hero, card
from utils.file_parser import extract_document


def render(state):
    hero("RESEARCH WORKSPACE", "Research Assistant", "Analyze papers, synthesize literature, compare methodologies, surface potential gaps, and generate research questions.")
    if state.get("llm") is None:
        st.warning("Configure GROQ_API_KEY before using Research Assistant.")
        return
    left, right = st.columns([1.0, 2.0])
    with left:
        st.markdown("<div class='section-label'>Research task</div>", unsafe_allow_html=True)
        mode = st.selectbox("Research mode", ["Paper Analyzer","Literature Review","Compare Papers","Research Gaps","Methodology Analysis","Research Questions","Key Findings"], label_visibility="collapsed")
        uploads = st.file_uploader("Research papers", type=["pdf","docx","txt"], accept_multiple_files=True, key="research_uploads")
        if uploads and st.button("Process papers", type="primary"):
            try:
                texts = []
                metas = []
                for upload in uploads:
                    result = extract_document(upload.name, upload.getvalue())
                    texts.append(f"===== {upload.name} =====\n{result.text}")
                    metas.append((upload.name, result.pages, result.ocr_pages, result.mode))
                state["research_material"] = "\n\n".join(texts)
                state["research_meta"] = metas
                st.success(f"Processed {len(texts)} paper(s).")
            except Exception as exc:
                st.error(str(exc))
        if state.get("research_meta"):
            for name, pages, ocr, mode_value in state["research_meta"]:
                st.caption(f"{name} · {pages} page(s) · OCR {ocr} · {mode_value}")
    with right:
        card("🔬", "Evidence-first research", "The assistant separates paper-supported findings from suggested research directions.")
        if state.get("research_material"):
            if st.button("Run research analysis", type="primary", use_container_width=True):
                with st.spinner("Analyzing research material…"):
                    try:
                        state["research_result"] = ResearchAssistant(state["llm"]).run(mode, state["research_material"])
                        state["research_mode_last"] = mode
                    except Exception as exc:
                        st.error(str(exc))
            if state.get("research_result"):
                st.markdown(f"### {state.get('research_mode_last', mode)}")
                st.markdown(state["research_result"])
                st.download_button("Download analysis", state["research_result"], file_name="research_analysis.md", mime="text/markdown")
        else:
            st.info("Upload one or more papers to activate the research workspace.")
