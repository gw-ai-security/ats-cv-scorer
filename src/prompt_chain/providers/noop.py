from __future__ import annotations

from src.prompt_chain.heuristics import (
    step1_match,
    step2_rewrite_suggestions,
    step3_ats_risks,
    step4_interview_questions,
)
from src.prompt_chain.providers.base import LLMProvider
from src.prompt_chain.models import Step1Result, Step2Result, Step3Result, Step4Result


class NoopProvider(LLMProvider):
    name = "fallback"

    def step1(self, resume_text: str, jd_text: str, language: str) -> Step1Result:
        return step1_match(resume_text, jd_text, language)

    def step2(self, resume_text: str, jd_text: str, language: str) -> Step2Result:
        return step2_rewrite_suggestions(resume_text, jd_text, language)

    def step3(self, resume_text: str, jd_text: str, language: str) -> Step3Result:
        return step3_ats_risks(resume_text, jd_text, language)

    def step4(self, resume_text: str, jd_text: str, language: str) -> Step4Result:
        return step4_interview_questions(resume_text, jd_text, language)
