from __future__ import annotations

from abc import ABC, abstractmethod

from src.prompt_chain.models import Step1Result, Step2Result, Step3Result, Step4Result


class LLMProvider(ABC):
    name: str = "base"

    @abstractmethod
    def step1(self, resume_text: str, jd_text: str, language: str) -> Step1Result:
        raise NotImplementedError

    @abstractmethod
    def step2(self, resume_text: str, jd_text: str, language: str) -> Step2Result:
        raise NotImplementedError

    @abstractmethod
    def step3(self, resume_text: str, jd_text: str, language: str) -> Step3Result:
        raise NotImplementedError

    @abstractmethod
    def step4(self, resume_text: str, jd_text: str, language: str) -> Step4Result:
        raise NotImplementedError
