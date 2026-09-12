import streamlit as st
from study.assistant import StudyAssistant
from ui.theme import hero, card
from utils.file_parser import extract_document


def render(state):
    hero(
        "LEARNING WORKSPACE",
        "Study Assistant",
        "Turn your notes and course material into explanations, flashcards, MCQs, quizzes, notes, and study plans.",
    )

    if state.get("llm") is None:
        st.warning("Configure GROQ_API_KEY before using Study Assistant.")
        return

    col1, col2 = st.columns([1.05, 1.95])

    with col1:
        st.markdown(
            "<div class='section-label'>Choose a study mode</div>",
            unsafe_allow_html=True,
        )

        mode = st.selectbox(
            "Study mode",
            [
                "Document Q&A",
                "Flashcards",
                "MCQ Lab",
                "Important Questions",
                "Smart Notes",
                "Summary",
                "Study Plan",
            ],
            label_visibility="collapsed",
        )

        difficulty = st.selectbox(
            "Difficulty",
            ["Balanced", "Easy", "Medium", "Hard"],
        )

        if mode == "MCQ Lab":
            count = st.slider("Questions", 5, 20, 10)
        else:
            count = None

        upload = st.file_uploader(
            "Study material",
            type=["pdf", "docx", "txt"],
            key="study_upload",
        )

        selected = state.get("study_material", "")

        if upload and st.button("Process material", type="primary"):
            try:
                result = extract_document(
                    upload.name,
                    upload.getvalue(),
                )
                state["study_material"] = result.text
                state["study_meta"] = result
                state["study_result"] = ""
                st.success(
                    f"Processed {upload.name} ({result.mode})."
                )
            except Exception as exc:
                st.error(str(exc))

        if selected:
            meta = state.get("study_meta")
            if meta:
                st.caption(
                    f"{meta.pages} page(s) · "
                    f"OCR pages: {meta.ocr_pages} · "
                    f"mode: {meta.mode}"
                )

    with col2:
        card(
            "🧠",
            "Grounded learning",
            "Every generated study artifact is based on the material you provide.",
        )

        if state.get("study_material"):

            # ---------------------------------------------------------
            # Document Q&A
            # ---------------------------------------------------------
            if mode == "Document Q&A":
                question = st.text_area(
                    "Your question",
                    placeholder=(
                        "Ask a question about your study material..."
                    ),
                    height=120,
                )

                if st.button(
                    "Ask Question",
                    type="primary",
                    use_container_width=True,
                ):
                    if not question.strip():
                        st.warning(
                            "Please enter a question before asking."
                        )
                    else:
                        settings = (
                            f"Difficulty: {difficulty}; "
                            f"User question: {question.strip()}"
                        )

                        with st.spinner(
                            "Searching your material and preparing an answer…"
                        ):
                            try:
                                state["study_result"] = StudyAssistant(
                                    state["llm"]
                                ).run(
                                    mode,
                                    state["study_material"],
                                    settings,
                                )
                                state["study_mode_last"] = mode
                            except Exception as exc:
                                st.error(str(exc))

            # ---------------------------------------------------------
            # All other study modes
            # ---------------------------------------------------------
            else:
                settings = (
                    f"Difficulty: {difficulty}; "
                    f"requested question count: "
                    f"{count or 'not applicable'}"
                )

                if st.button(
                    "Generate",
                    type="primary",
                    use_container_width=True,
                ):
                    with st.spinner(
                        "Building your study material…"
                    ):
                        try:
                            state["study_result"] = StudyAssistant(
                                state["llm"]
                            ).run(
                                mode,
                                state["study_material"],
                                settings,
                            )
                            state["study_mode_last"] = mode
                        except Exception as exc:
                            st.error(str(exc))

            # ---------------------------------------------------------
            # Display result
            # ---------------------------------------------------------
            if state.get("study_result"):
                st.markdown(
                    f"### {state.get('study_mode_last', mode)}"
                )
                st.markdown(state["study_result"])

                st.download_button(
                    "Download result",
                    state["study_result"],
                    file_name="study_output.md",
                    mime="text/markdown",
                )

        else:
            st.info(
                "Upload study material to activate the workspace."
            )