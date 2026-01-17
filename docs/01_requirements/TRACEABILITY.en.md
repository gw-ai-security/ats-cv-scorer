# Traceability Matrix (v0)

| Requirement | Implementation | Tests |
|------------|----------------|-------|
| FR-001 | src/utils/validation.py, frontend/streamlit_app.py | tests/integration/test_upload_validation.py |
| FR-002 | src/core/pdf_processor.py | tests/unit/test_pdf_processor.py |
| FR-003 | src/core/cv_analyzer.py | tests/unit/test_cv_sections.py |
| FR-004 | src/core/skill_extractor.py | tests/unit/test_skill_extractor.py |
| FR-005 | src/core/ats_criteria_extractor.py | tests/unit/test_ats_criteria.py |
| FR-006 | src/core/jd_parser.py | tests/unit/test_jd_parser.py |
| FR-007 | src/core/matcher.py, frontend/streamlit_app.py | tests/unit/test_matcher.py |
| FR-008 | docs/02_architecture/ADR/ADR-002-ml-matching.md | n/a |
