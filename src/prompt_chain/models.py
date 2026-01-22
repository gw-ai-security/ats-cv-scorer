from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


CHAIN_VERSION = "1.0.0"


@dataclass(frozen=True)
class PromptChainSettings:
    language: str = "unknown"
    use_llm: bool = False
    provider: str = "fallback"


@dataclass(frozen=True)
class Step1Result:
    score_0_100: float
    missing_keywords: list[str]
    rationale: str


@dataclass(frozen=True)
class Step2Result:
    rewrite_mode: str
    templates: list[str]
    evidence_refs: list[str]
    warnings: list[str]


@dataclass(frozen=True)
class Step3Result:
    issues: list[str]
    fixes: list[str]


@dataclass(frozen=True)
class Step4QA:
    question: str
    answer: str
    evidence_refs: list[str]
    insufficient_evidence: bool


@dataclass(frozen=True)
class Step4Result:
    questions: list[Step4QA]


@dataclass(frozen=True)
class SafetyFlags:
    pii_detected_counts: dict[str, int]
    invented_claims_blocked: int
    missing_evidence_warnings: int


@dataclass(frozen=True)
class PromptChainResult:
    chain_run_id: str
    timestamp: str
    app_version: str
    strategy: str
    inputs: dict[str, Any]
    step_results: dict[str, Any]
    safety_flags: SafetyFlags

    @staticmethod
    def now_timestamp() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
