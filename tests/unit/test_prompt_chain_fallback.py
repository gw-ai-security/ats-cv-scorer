from __future__ import annotations

from src.prompt_chain.engine import run_prompt_chain
from src.prompt_chain.models import PromptChainSettings


def test_prompt_chain_fallback_outputs() -> None:
    resume_text = "Profile: Backend engineer with Python and SQL. Experience: Built APIs."
    jd_text = "Backend Engineer role. Required: Python, SQL, Docker, AWS."

    settings = PromptChainSettings(language="en", use_llm=False, provider="fallback")
    result = run_prompt_chain(resume_text, jd_text, settings)

    step1 = result.step_results["step1"]
    assert 0 <= step1["score_0_100"] <= 100
    assert len(step1["missing_keywords"]) == 5

    step2 = result.step_results["step2"]
    assert step2["rewrite_mode"] == "templates_only"
    assert step2["templates"]

    step3 = result.step_results["step3"]
    assert step3["issues"]

    step4 = result.step_results["step4"]
    assert len(step4["questions"]) == 3
    for qa in step4["questions"]:
        assert "question" in qa and "answer" in qa
