# Prompt Chain Workflow (EN)

## What it does
A guided 4-step workflow that turns a CV + JD into actionable improvements, ATS fixes, and interview preparation.

## Steps
1) Recruiter Match: score and top 5 missing keywords.
2) Experience Rewrite: XYZ templates with evidence requirements.
3) ATS Parse Check: detect parsing risks and fixes.
4) Interview Stress Test: 3 hard questions + answers from resume evidence.

## Modes
- **Fallback**: deterministic heuristics; works offline.
- **LLM (optional)**: uses provider interface if configured; must obey no-invention rules.

## Evidence Policy
- Each rewrite suggestion and answer must include evidence references or be marked as insufficient evidence.
- No new claims are invented.

## Exports
Prompt Chain results are included in PDF/JSON/MD reports.

## References
- `docs/codex_skills/SKILL_PROMPT_CHAIN_WORKFLOW.md`
- `src/prompt_chain/`

## Last Updated
2026-01-22 21:00:00 (Local)
