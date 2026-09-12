import streamlit as st
from features.resume_generator import ResumeGenerator
from features.evidence import source_labels
from ui.theme import hero


def render(state):
    hero("CAREER", "Resume Studio", "Create a tailored resume from your verified evidence without fabricating jobs, projects, skills, metrics or credentials.")
    if not state.get("opportunity_text"):
        st.info("Analyze an opportunity first."); return
    if not state.get("profile_manager") or state["profile_manager"].store.is_empty:
        st.info("Build your personal knowledge base first."); return
    if state.get("llm") is None:
        st.warning("Configure GROQ_API_KEY first."); return
    if st.button("Generate tailored resume", type="primary", use_container_width=True):
        with st.spinner("Selecting relevant evidence and drafting your resume…"):
            try:
                resume, evidence = ResumeGenerator(state["llm"], state["retriever"]).generate(state["opportunity_text"])
                state["resume"], state["resume_evidence"] = resume, evidence
            except Exception as exc: st.error(str(exc))
    if state.get("resume"):
        st.markdown("### Resume preview")
        st.markdown(state["resume"])
        st.download_button("Download Markdown", state["resume"], file_name="tailored_resume.md", mime="text/markdown")
        st.markdown("### Evidence used")
        for src in source_labels(state.get("resume_evidence", [])): st.write(f"- {src}")
