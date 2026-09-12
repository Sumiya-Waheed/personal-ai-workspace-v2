from __future__ import annotations
from llm.generator import research_generate

TASKS = {
    "Paper Analyzer": "Produce a research snapshot: research problem, objective, methodology, data/dataset, findings, limitations, and conclusion. Preserve uncertainty where the paper is unclear.",
    "Literature Review": "Synthesize the supplied papers into themes, methods, findings, limitations, agreements, contradictions, and potential gaps. Do not invent bibliographic details.",
    "Compare Papers": "Compare the supplied papers by research question, methodology, data, results, strengths, limitations, and conclusions. Use a compact structured format.",
    "Research Gaps": "Identify potential research gaps supported by the supplied material. For each gap, explain the evidence and label proposed directions as suggestions.",
    "Methodology Analysis": "Analyze the methodology, study design, data, evaluation approach, and stated limitations. Explain what is actually supported by the material.",
    "Research Questions": "Generate potential research questions inspired by the supplied material. Separate evidence-backed observations from new suggested questions.",
    "Key Findings": "Extract the most important findings and supporting evidence from the supplied material, keeping the wording concise and grounded.",
}

class ResearchAssistant:
    def __init__(self, llm):
        self.llm = llm

    def run(self, mode: str, material: str, settings: str = "") -> str:
        if mode not in TASKS:
            raise ValueError("Unsupported research mode.")
        return research_generate(self.llm, TASKS[mode], material, settings)
