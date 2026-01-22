# Release Notes vNext

## Highlights
- External dataset ingestion from local Kaggle ZIPs with registry metadata and ingest reporting.
- External data quality and PII scan reports (no raw data committed).
- Optional calibrator training with documented feature set.
- Report exports: PDF + JSON + Markdown.
- Streamlit demo mode with synthetic fixtures and export buttons.

## vNext.1 Updates
- License registry workflow with overrides + changelog.
- Hybrid ML external evaluation skips gracefully when embeddings are unavailable.
- Adapter validation fixtures/tests + adapter health report.
- Prompt Chain workflow with offline fallback, optional LLM provider, and exports.

## Governance
- External datasets default to `restricted` until license verification.
- Evaluation gate remains enforced for hybrid ML.

## Known Limitations
- Hybrid ML evaluation on external data may be skipped if embedding models are unavailable.
- Dataset adapters require per-dataset validation; some fields are heuristic mappings.

## References
- `docs/00_overview/VNEXT_ACCEPTANCE_CHECKLIST.md`
- `docs/02_architecture/ADR/ADR-003-external-datasets.md`
- `docs/02_architecture/ADR/ADR-004-reporting-and-exports.md`
