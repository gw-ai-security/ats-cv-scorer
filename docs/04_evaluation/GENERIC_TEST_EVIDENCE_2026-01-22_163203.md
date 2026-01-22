# Generic Test Evaluation Evidence

Run timestamp: 2026-01-22 16:35:18 (Local)

## Inputs
- CV: `generic test files\cvs\Curriculum Vitae.txt`
- JD: `generic test files\job descriptions\01 - Job Title Software Engineer.txt`

## CV Sections
- headers_found: ['experience', 'education', 'skills']

- contact: Curriculum Vitae Name: Alex Morgan Profile: Detail-oriented Software Engineer with a strong focus on backend development, data processing, and code quality. Experienced in building maintainable softwa
- experience: Software Engineer TechSolutions GmbH 2021 – Present - Developed backend components using Python - Implemented data-processing pipelines for internal tools - Wrote unit and integration tests to ensure 
- education: Bachelor of Science in Business Informatics University of Applied Sciences 2016 – 2019
- skills: Programming Languages: - Python - SQL (basic) Software Engineering: - Backend development - Modular software design - Unit testing - Integration testing Tools and Technologies: - Git - CI/CD pipelines
- projects: 

## Skill Extraction
- skills: {"technical": ["python", "sql"], "soft": [], "languages": ["english", "german"], "certifications": []}

## ATS Criteria
- contact: {'name': 'Curriculum Vitae', 'email': 'not_found', 'phone': 'not_found', 'location': 'not_found', 'links': 'not_found'}
- summary: Detail-oriented Software Engineer with a strong focus on backend development, data processing, and code quality. Experienced in building maintainable software systems with an emphasis on transparency, testing, and documentation.
- experience_count: 3
- education_count: 2
- skills: {'hard': ['python', 'sql'], 'soft': [], 'languages': ['english', 'german'], 'certifications': [], 'tools': ['git'], 'methods': []}
- certifications: []
- languages: ['german', 'english']
- availability: not_found
- missing_fields: ['contact.email', 'contact.phone', 'contact.location', 'contact.links', 'certifications', 'availability']

## JD Parse Result
- role: Software Engineer (Backend / Data-Focused)
- seniority: mid
- location: not_found
- remote: no
- skills: ['python']
- keywords: []
- requirements: []
- responsibilities: []

## Match Result (Baseline)
- score: 100.0
- breakdown: {'skills': {'matched': ['python'], 'gaps': [], 'evidence_ratio': 1.0, 'unverified_skills': [], 'evidence_snippets': {'python': 'evidence_found'}, 'score': 1.0}, 'experience': {'seniority': 'mid', 'has_experience': True, 'score': 1.0}, 'education': {'note': 'no_degree_requirement', 'score': 1.0}, 'language': {'note': 'no_language_requirement', 'score': 1.0}, 'location': {'note': 'no_location_requirement', 'score': 1.0}, 'penalties': {'missing_required_skills': [], 'missing_required_count': 0, 'keyword_stuffing_risk': False, 'unverified_skill_count': 0, 'evidence_ratio': 1.0}}

## Score Rationale
- Score is weighted by skills/experience/education/language/location per baseline rules.
- Skill matches, gaps, and penalties are visible in the breakdown above.