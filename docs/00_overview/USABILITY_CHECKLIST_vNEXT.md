# vNext Usability Checklist (Manual)

## Goal
Verify the 60-second Streamlit demo flow with PDF/JSON/MD exports.

## Preconditions
- Dependencies installed (`pip install -r requirements.txt`).
- Evaluation gate documented (see `docs/04_evaluation/EVALUATION_RESULTS.md`).

## Steps and Expected Outputs
1) Launch the app
```
$env:PYTHONPATH='.'; py -m streamlit run frontend/streamlit_app.py
```
Expected:
- App loads at `http://localhost:8501`.

2) Enable Demo Mode
- Toggle: `Demo mode (synthetic fixtures)`
- Select a `Demo pair` (e.g., `pair_0001`)
Expected:
- CV text loads without upload.
- JD text is parsed automatically.

3) Run Matching
- Ensure `Run analysis` and `Run matching` are enabled.
- Select strategy: `rule_based` (default).
Expected:
- Match score shown.
- Breakdown displayed.
- Warnings shown if extraction quality is low.

4) Explainability
- Open `Match` tab.
Expected:
- Missing required skills and evidence snippets appear.
- Penalties displayed (keyword stuffing risk, missing required).

5) Export Reports
- Click download buttons:
  - `Download score report (PDF)`
  - `Download score report (JSON)`
  - `Download score report (MD)`
Expected:
- Files download successfully and reflect the same score/breakdown.

6) Strategy Gate
- If evaluation gate is open, switch to `hybrid_ml`.
Expected:
- ML explanation shows semantic similarity and top matched chunks.
- If gate is closed, UI shows warning and only `rule_based`.

## Pass Criteria
- All steps complete within ~60 seconds.
- PDF/JSON/MD exports are consistent and readable.
- No crashes during demo flow.
