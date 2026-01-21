# Definition of Done - vNext

## Scope
Applies to the vNext release with external data ingestion, reporting exports, and demo readiness.

## Criteria
- External dataset ingestion works offline with local ZIPs.
- Raw datasets are excluded from git; only registry + reports are committed.
- License status defaults to `restricted` until verified and documented.
- External data quality + PII scan reports are generated.
- External evaluation summary is documented with limitations.
- Report exports are available in PDF/JSON/MD.
- Streamlit demo runs within 60 seconds using synthetic fixtures.
- Hybrid ML remains gated by evaluation results.
- Tests added for registry/adapters and report export schema.

## References
- `docs/00_overview/VNEXT_ACCEPTANCE_CHECKLIST.md`
- `docs/02_architecture/ADR/ADR-003-external-datasets.md`
- `docs/02_architecture/ADR/ADR-004-reporting-and-exports.md`
