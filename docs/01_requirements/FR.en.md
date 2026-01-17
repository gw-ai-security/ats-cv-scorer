# Functional Requirements (FR)

## FR-001 PDF Upload and Validation
Priority: MUST
Status: DONE
Acceptance:
- accept PDF up to 10MB
- validate file type
- show clear, user-friendly errors

## FR-002 Text Extraction (Phase 1)
Priority: MUST
Status: DONE
Depends on: FR-001
Acceptance:
- use pdfplumber as primary extractor
- deterministic behavior for the same input
- extraction metadata: method, page_count, word_count, quality
- graceful failure handling (no crash, empty text + error)
- OCR fallback is explicitly out of scope for Phase 1

## FR-003 CV Structure Analysis
Priority: MUST
Status: DONE
Acceptance:
- detect sections: contact, experience, education, skills, projects
- support DE/EN headers
- graceful degradation

## FR-004 Skill Extraction and Categorization
Priority: MUST
Status: DONE
Acceptance:
- skill DB support
- synonyms (e.g., JS -> JavaScript)
- categories: technical, soft, languages, certifications

## FR-005 Extract ATS recruiter criteria from CV
Priority: MUST
Status: DONE
Acceptance:
- Contact: name, email, phone, location, links (LinkedIn/GitHub/portfolio)
- Summary/profile detected if present
- Experience: role, company, timeframe, key responsibilities
- Education: degree, institution, timeframe
- Skills: hard/soft/tools/methods
- Certifications and languages detected
- Availability/notice period detected if present
- Missing fields are marked "not found" (no crash)

## FR-006 Job description upload and parsing
Priority: MUST
Status: DONE
Acceptance:
- JD upload (PDF)
- Extracted fields: role, seniority, location/remote, requirements, nice-to-have, responsibilities
- Requirements mapped to structured skill and keyword lists
- Support DE/EN headers
- Graceful degradation

## FR-007 CV <-> JD matching (baseline, rules-based)
Priority: MUST
Status: DONE
Depends on: FR-005, FR-006
Acceptance:
- Score with explainable rationale (match/gap per criterion)
- Configurable weighting (e.g., skills, experience, education, language)
- Missing information surfaced explicitly
- Deterministic behavior for the same input

## FR-008 Plan ML approach for matching
Priority: SHOULD
Status: PLANNED
Acceptance:
- Documented ML plan (data needs, features, model families)
- Evaluation metrics (precision/recall, ranking, human review)
- Bias and privacy risks documented
- Rollout plan (baseline -> ML experiments)
