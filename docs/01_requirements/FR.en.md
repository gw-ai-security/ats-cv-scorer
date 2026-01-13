# Functional Requirements (FR)

## FR-001 PDF Upload & Validation
Priority: MUST
Status: PLANNED
Acceptance:
- Accept PDF up to 10MB
- Validate file type
- Clear user-friendly error messages

## FR-002 Multi-Strategy Text Extraction
Priority: MUST
Status: PLANNED
Depends on: FR-001
Acceptance:
- pdfplumber primary
- OCR fallback when extracted words < 50
- extraction metadata: method, page_count, quality

## FR-003 CV Structure Analysis
Priority: MUST
Status: PLANNED
Acceptance:
- detect sections: contact, experience, education, skills, projects
- support DE/EN headers
- graceful degradation

## FR-004 Skill Extraction & Categorization
Priority: MUST
Status: PLANNED
Acceptance:
- skill DB support
- synonyms (e.g., JS → JavaScript)
- categories: technical, soft, languages, certifications
