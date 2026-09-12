import streamlit as st
from utils.file_parser import extract_document
from utils.validators import validate_upload
from opportunity.analyzer import OpportunityAnalyzer
from ui.theme import hero


def render(state):
    hero("CAREER", "Opportunity Intelligence", "Upload a scholarship, job, internship, fellowship or university opportunity and extract only what it actually requires.")
    upload = st.file_uploader("Opportunity document", type=["pdf","docx","txt"], key="opportunity_uploader")
    if upload:
        ok, msg = validate_upload(upload.name, upload.size)
        if not ok:
            st.error(msg); return
        if st.button("Analyze opportunity", type="primary", use_container_width=True):
            if state.get("llm") is None:
                st.error("Configure GROQ_API_KEY first."); return
            with st.spinner("Reading the opportunity and extracting explicit requirements…"):
                try:
                    result = extract_document(upload.name, upload.getvalue())
                    state["opportunity_text"] = result.text
                    state["opportunity_meta"] = result
                    state["opportunity_analysis"] = OpportunityAnalyzer(state["llm"]).analyze(result.text)
                    state["match_result"] = None
                    st.success(f"Opportunity analyzed · {result.pages} page(s) · {result.mode} extraction.")
                except Exception as exc:
                    st.error(str(exc))
    analysis = state.get("opportunity_analysis")
    if analysis:
        st.markdown("<div class='section-label'>Opportunity intelligence</div>", unsafe_allow_html=True)
        labels = [
            ("Opportunity type","opportunity_type"),("Eligibility","eligibility_requirements"),
            ("Education","education_requirements"),("Required skills","required_skills"),
            ("Required experience","required_experience"),("Preferred qualifications","preferred_qualifications"),
            ("Documents required","documents_required"),("Important criteria","important_criteria"),
            ("Application questions","application_questions"),("Other requirements","other_requirements")]
        for title, key in labels:
            value = analysis.get(key, [])
            if value:
                with st.expander(title, expanded=title in ("Opportunity type","Eligibility","Required skills")):
                    if isinstance(value, list):
                        for item in value: st.markdown(f"- {item}")
                    else: st.write(value)
