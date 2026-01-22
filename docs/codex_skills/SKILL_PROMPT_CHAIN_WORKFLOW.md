# Skill: Prompt Chain Workflow

## Purpose
Provide a guided, explainable 4-step workflow to help users improve a CV for a specific JD, with offline fallback and optional LLM support.

## When to Use
- When a user wants actionable CV improvements beyond a single match score.
- When explainable, auditable outputs are required for review.

## Steps
1) Recruiter Match: score + top 5 missing keywords.
2) Experience Rewrite: XYZ templates + evidence requirements.
3) ATS Parse Check: issues + fixes for ATS readability.
4) Interview Stress Test: 3 hard questions + answers from evidence.

## Definition of Done
- Runs offline in fallback mode.
- LLM usage is optional and clearly indicated.
- Outputs include evidence references and safety flags.
- PDF/JSON/MD exports include the chain results.

## Extension Points
- Add new providers under `src/prompt_chain/providers/`.
- Update heuristics in `src/prompt_chain/heuristics.py`.
- Update tests to keep outputs stable.

## References
- `src/prompt_chain/`
- `frontend/streamlit_app.py`
- `docs/knowledge_base/en/10_prompt_chain_workflow.md`
