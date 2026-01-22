from __future__ import annotations

import os
import uuid

from src.prompt_chain.heuristics import compute_pii_counts, hash_text
from src.prompt_chain.models import (
    CHAIN_VERSION,
    PromptChainResult,
    PromptChainSettings,
    SafetyFlags,
)
from src.prompt_chain.providers.noop import NoopProvider
from src.prompt_chain.providers.openai_provider import OpenAIProvider


def _select_provider(settings: PromptChainSettings):
    if settings.use_llm:
        try:
            return OpenAIProvider()
        except Exception:
            return NoopProvider()
    return NoopProvider()


def run_prompt_chain(
    resume_text: str,
    jd_text: str,
    settings: PromptChainSettings,
    app_version: str = "vNext",
) -> PromptChainResult:
    provider = _select_provider(settings)
    step1 = provider.step1(resume_text, jd_text, settings.language)
    step2 = provider.step2(resume_text, jd_text, settings.language)
    step3 = provider.step3(resume_text, jd_text, settings.language)
    step4 = provider.step4(resume_text, jd_text, settings.language)

    pii_counts = compute_pii_counts(resume_text + " " + jd_text)
    missing_evidence = sum(
        1 for item in step4.questions if item.insufficient_evidence
    ) + len([template for template in step2.templates if "evidence" in template.lower()])

    safety = SafetyFlags(
        pii_detected_counts=pii_counts,
        invented_claims_blocked=0,
        missing_evidence_warnings=missing_evidence,
    )

    inputs = {
        "resume_text_hash": hash_text(resume_text),
        "jd_text_hash": hash_text(jd_text),
        "language": settings.language,
        "settings": {
            "use_llm": settings.use_llm,
            "provider": provider.name,
        },
    }
    step_results = {
        "step1": step1.__dict__,
        "step2": step2.__dict__,
        "step3": step3.__dict__,
        "step4": {
            "questions": [item.__dict__ for item in step4.questions],
        },
    }
    return PromptChainResult(
        chain_run_id=str(uuid.uuid4()),
        timestamp=PromptChainResult.now_timestamp(),
        app_version=app_version,
        strategy=provider.name,
        inputs=inputs,
        step_results=step_results,
        safety_flags=safety,
    )
