from __future__ import annotations

from src.prompt_chain.engine import run_prompt_chain
from src.prompt_chain.models import PromptChainSettings


def test_prompt_chain_schema_fields() -> None:
    resume_text = "Profile: Data engineer. Experience: ETL pipelines."
    jd_text = "Data Engineer role. Required: Python, SQL."
    settings = PromptChainSettings(language="en", use_llm=False, provider="fallback")
    result = run_prompt_chain(resume_text, jd_text, settings)

    assert result.chain_run_id
    assert result.timestamp
    assert result.app_version
    assert result.strategy
    assert "resume_text_hash" in result.inputs
    assert "jd_text_hash" in result.inputs
    assert "step1" in result.step_results
    assert "step2" in result.step_results
    assert "step3" in result.step_results
    assert "step4" in result.step_results
