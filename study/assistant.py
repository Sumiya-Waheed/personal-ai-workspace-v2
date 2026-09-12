from __future__ import annotations
from llm.generator import study_generate

TASKS = {
    "Document Q&A": "Answer the user's study question using the material. Explain clearly and cite page labels when present.",
    "Flashcards": "Create 12 high-quality flashcards. Format each as Q: ... / A: ... / Difficulty: Easy|Medium|Hard.",
    "MCQ Lab": "Create 10 MCQs with four options, correct answer, and a short explanation. Cover the most important concepts.",
    "Important Questions": "Identify 10 important exam/revision questions from the material and briefly explain why each matters.",
    "Smart Notes": "Turn the material into structured revision notes with headings, key concepts, definitions, formulas/examples when present, and common confusions.",
    "Summary": "Create a concise but comprehensive study summary with key takeaways and a final quick-review checklist.",
    "Study Plan": "Create a practical 7-day study plan based only on the material, organizing topics from foundational to advanced.",
}

class StudyAssistant:
    def __init__(self, llm):
        self.llm = llm

    def run(self, mode: str, material: str, settings: str = "") -> str:
        if mode not in TASKS:
            raise ValueError("Unsupported study mode.")
        return study_generate(self.llm, TASKS[mode], material, settings)
