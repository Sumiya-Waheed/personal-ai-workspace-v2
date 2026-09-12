import streamlit as st
from ui.theme import hero, metric, card


def render(state):
    name = "there"
    try:
        from auth import user_name
        name = user_name()
    except Exception:
        pass
    hero("PERSONAL AI WORKSPACE", f"Good to see you, {name} 👋", "One workspace for your career, study and research — grounded in the documents you provide.")
    docs = state.get("profile_docs", [])
    analysis = state.get("opportunity_analysis")
    match = state.get("match_result")
    cols = st.columns(4)
    with cols[0]: metric("Profile documents", str(len(docs)))
    with cols[1]: metric("Evidence chunks", str(len(state.get("profile_manager").store.records) if state.get("profile_manager") else 0))
    with cols[2]: metric("Opportunity", "Ready" if analysis else "—")
    with cols[3]: metric("Readiness", f"{match['_readiness']}%" if match else "—")

    st.markdown("<div class='section-label'>Explore your workspace</div>", unsafe_allow_html=True)
    grid = st.columns(3)
    cards = [
        ("💼", "Career Intelligence", "Build your profile, analyze opportunities, match evidence and tailor applications."),
        ("📚", "Study Assistant", "Turn notes and PDFs into flashcards, MCQs, summaries, important questions and study plans."),
        ("🔬", "Research Assistant", "Analyze papers, compare methods, synthesize literature and explore research gaps."),
    ]
    for col, (icon, title, desc) in zip(grid, cards):
        with col: card(icon, title, desc)

    st.markdown("<div class='section-label'>Recommended demo flow</div>", unsafe_allow_html=True)
    steps = st.columns(5)
    labels = [("01", "Build profile"), ("02", "Analyze opportunity"), ("03", "Match evidence"), ("04", "Generate answer"), ("05", "Tailor resume")]
    for col, (num, label) in zip(steps, labels):
        with col:
            st.markdown(f"<div class='card'><span class='pill'>{num}</span><h3>{label}</h3><p>Evidence-first workflow.</p></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-label'>Privacy</div>", unsafe_allow_html=True)
    st.info("Your uploaded documents are used to build the current session's knowledge base. Never upload passwords, payment information, API keys, or credentials.")
