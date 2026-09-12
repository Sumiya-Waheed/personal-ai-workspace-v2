import streamlit as st
from features.application_assistant import ApplicationAssistant
from features.evidence import source_labels
from ui.theme import hero


def render(state):
    hero("CAREER", "Application Assistant", "Generate polished answers from retrieved profile evidence instead of making the AI guess who you are.")
    if not state.get("opportunity_text"):
        st.info("Analyze an opportunity first."); return
    if not state.get("profile_manager") or state["profile_manager"].store.is_empty:
        st.info("Build your personal knowledge base first."); return
    if state.get("llm") is None:
        st.warning("Configure GROQ_API_KEY first."); return
    for msg in state.get("chat_history", []):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources"):
                st.caption("Evidence used")
                for src in msg["sources"]: st.write(f"- {src}")
    question = st.chat_input("Ask an application question…")
    if question:
        state["chat_history"].append({"role":"user","content":question})
        with st.chat_message("user"): st.markdown(question)
        with st.chat_message("assistant"):
            with st.spinner("Retrieving profile evidence…"):
                try:
                    answer, evidence = ApplicationAssistant(state["llm"], state["retriever"]).answer(question, state["opportunity_text"])
                    sources = source_labels(evidence)
                    st.markdown(answer)
                    st.caption("Evidence used")
                    for src in sources: st.write(f"- {src}")
                    state["chat_history"].append({"role":"assistant","content":answer,"sources":sources})
                except Exception as exc: st.error(str(exc))
    last = next((m for m in reversed(state.get("chat_history", [])) if m["role"] == "assistant"), None)
    if last:
        st.markdown("### Refine latest answer")
        cols = st.columns(4)
        for col, (label, instruction) in zip(cols, [("Shorter","Make this answer more concise."),("Formal","Make this answer more formal."),("Personal","Make this answer more personal without adding facts."),("Clearer","Improve clarity without adding facts.")]):
            with col:
                if st.button(label, use_container_width=True):
                    try:
                        answer, evidence = ApplicationAssistant(state["llm"], state["retriever"]).refine(last["content"], instruction)
                        state["chat_history"].append({"role":"assistant","content":answer,"sources":source_labels(evidence)})
                        st.rerun()
                    except Exception as exc: st.error(str(exc))
