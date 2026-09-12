"""Personal AI Workspace — Streamlit entry point and UI wiring only."""
from __future__ import annotations
import streamlit as st
from config import APP_NAME, TOP_K
from auth import auth_configured, require_login, user_name, user_email
from rag.embeddings import EmbeddingService
from rag.retriever import Retriever
from llm.groq_client import GroqClient
from candidate_profile.profile_manager import ProfileManager
from ui import dashboard, profile_page, opportunity_page, match_page, assistant_page, resume_page, study_page, research_page
from ui.theme import inject

st.set_page_config(page_title=APP_NAME, page_icon="✦", layout="wide", initial_sidebar_state="expanded")
inject()


def login_screen():
    st.markdown('<div class="login-wrap"><div class="login-panel">', unsafe_allow_html=True)
    st.markdown("<div class='hero-kicker'>PERSONAL AI WORKSPACE</div>", unsafe_allow_html=True)
    st.markdown("# Welcome back")
    st.markdown("Your evidence-grounded workspace for **career, learning and research**.")
    st.write("")
    st.button("Continue with Google", type="primary", use_container_width=True, on_click=st.login)
    st.caption("Secure sign-in powered by Streamlit OpenID Connect.")
    st.markdown('</div></div>', unsafe_allow_html=True)


if auth_configured() and not require_login():
    login_screen()
    st.stop()

@st.cache_resource(show_spinner="Loading the AI embedding model…")
def get_embeddings():
    return EmbeddingService()


def init_state():
    if "profile_manager" not in st.session_state:
        embeddings = get_embeddings()
        st.session_state.profile_manager = ProfileManager(embeddings)
        st.session_state.retriever = Retriever(st.session_state.profile_manager.store, embeddings)
    if "llm" not in st.session_state:
        try:
            st.session_state.llm = GroqClient()
            st.session_state.llm_error = None
        except Exception as exc:
            st.session_state.llm = None
            st.session_state.llm_error = str(exc)
    defaults = {
        "profile_docs": [], "profile_files": [], "opportunity_text": None,
        "opportunity_analysis": None, "match_result": None, "resume": None,
        "resume_evidence": [], "chat_history": [], "study_material": None,
        "study_result": None, "research_material": None, "research_result": None,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


init_state()

pages = {
    "Home": dashboard.render,
    "My Profile": profile_page.render,
    "Opportunities": opportunity_page.render,
    "Match Analysis": match_page.render,
    "Application Assistant": assistant_page.render,
    "Resume Studio": resume_page.render,
    "Study Assistant": study_page.render,
    "Research Assistant": research_page.render,
}

with st.sidebar:
    st.markdown("# ✦ Personal AI")
    st.caption("Career · Learning · Research")
    if auth_configured():
        st.success(f"Signed in as {user_name()}")
        if user_email():
            st.caption(user_email())
        if st.button("Log out", use_container_width=True):
            st.logout()
    else:
        st.info("Preview mode")
        st.caption("Add OIDC secrets to enable Google login.")
    if st.session_state.get("llm") is None:
        st.error("Groq API key is not configured.")
        st.caption("Add GROQ_API_KEY to Streamlit Secrets.")
    st.divider()
    st.markdown("**CAREER**")
    career = ["My Profile", "Opportunities", "Match Analysis", "Application Assistant", "Resume Studio"]
    st.markdown("**LEARNING**")
    learning = ["Study Assistant"]
    st.markdown("**RESEARCH**")
    research = ["Research Assistant"]
    options = ["Home"] + career + learning + research
    page = st.radio("Workspace", options, label_visibility="collapsed")
    st.divider()
    st.caption(f"RAG top-k · {TOP_K}")
    st.caption("Personal documents stay in the current session unless you add a persistent storage layer.")

pages[page](st.session_state)
