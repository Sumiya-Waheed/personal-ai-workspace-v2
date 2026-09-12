import streamlit as st
from opportunity.matcher import OpportunityMatcher
from features.readiness_score import calculate_readiness
from ui.theme import hero, metric


def render(state):
    hero("CAREER", "Match Analysis", "See how your verified profile evidence aligns with the opportunity — including matches, gaps and uncertainty.")
    if not state.get("opportunity_analysis"):
        st.info("Analyze an opportunity first."); return
    if not state.get("profile_manager") or state["profile_manager"].store.is_empty:
        st.info("Build your personal knowledge base first."); return
    if state.get("llm") is None:
        st.warning("Configure GROQ_API_KEY first."); return
    if st.button("Run profile ↔ opportunity match", type="primary", use_container_width=True):
        with st.spinner("Retrieving evidence and comparing requirements…"):
            try:
                evidence = OpportunityMatcher(state["llm"], state["retriever"]).retrieve_for_analysis(state["opportunity_analysis"])
                result = OpportunityMatcher(state["llm"], state["retriever"]).match(state["opportunity_analysis"], evidence)
                score, category_scores = calculate_readiness(result)
                result["_evidence"], result["_readiness"], result["_category_scores"] = evidence, score, category_scores
                state["match_result"] = result
            except Exception as exc: st.error(str(exc))
    result = state.get("match_result")
    if not result: return
    score = result["_readiness"]
    st.markdown("### Application readiness")
    st.progress(score / 100)
    st.markdown(f"<div class='card'><div class='metric-value'>{score}%</div><p>AI-generated profile match/readiness estimate — not a scientifically validated probability.</p></div>", unsafe_allow_html=True)
    cols = st.columns(5)
    for col, (label, key) in zip(cols, [("Eligibility","eligibility"),("Skills","skills"),("Experience","experience"),("Documents","documents"),("Other","other")]):
        with col: metric(label, f"{result['_category_scores'][key]}%")
    for title, key, icon in [("Matches","matches","✓"),("Gaps / missing information","gaps","⚠"),("Unclear","unclear","?")]:
        st.markdown(f"### {icon} {title}")
        items = result.get(key, [])
        if items:
            for item in items: st.write(f"- {item}")
        else: st.write("None identified.")
    st.markdown("### Evidence")
    for item in result.get("_evidence", []):
        with st.expander(f"{item['source']} · similarity {item['score']:.2f}"):
            st.write(item["text"])
