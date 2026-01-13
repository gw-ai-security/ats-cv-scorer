# Functional Requirements (FR)

## FR-001 PDF Upload and Validation
Priority: MUST
Status: PLANNED
Acceptance:
- accept PDF up to 10MB
- validate file type
- show clear, user-friendly errors

## FR-002 Text Extraction (Phase 1)
Priority: MUST
Status: IN PROGRESS
Depends on: FR-001
Acceptance:
- use pdfplumber as primary extractor
- deterministic behavior for the same input
- extraction metadata: method, page_count, word_count, quality
- graceful failure handling (no crash, empty text + error)
- OCR fallback is explicitly out of scope for Phase 1

## FR-003 CV Structure Analysis
Priority: MUST
Status: PLANNED
Acceptance:
- detect sections: contact, experience, education, skills, projects
- support DE/EN headers
- graceful degradation

## FR-004 Skill Extraction and Categorization
Priority: MUST
Status: PLANNED
Acceptance:
- skill DB support
- synonyms (e.g., JS -> JavaScript)
- categories: technical, soft, languages, certifications
