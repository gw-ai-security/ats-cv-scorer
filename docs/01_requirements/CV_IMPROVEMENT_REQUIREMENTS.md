# CV Improvement Requirements Catalog

## Purpose
Define the minimum CV requirements and skill evidence rules used by ATS CV Scorer to generate improvement guidance.

## Required CV Sections
1) Contact: name, email, phone, location.
2) Summary/Profile: 2-4 sentences aligned to the target JD.
3) Experience: role, company, timeframe, responsibilities.
4) Education: degree, institution, timeframe (if JD requires a degree).
5) Skills: grouped list of technical and soft skills.
6) Languages: list with proficiency if required by the JD.
7) Certifications (optional but recommended if listed in JD).
8) Availability (optional; required if JD requests it).

## Skill Evidence Rules
- Skills listed in the Skills section must be evidenced in Experience or Projects.
- Each required JD skill should appear in at least one Experience/Project bullet.
- Skills without evidence are treated as lower confidence and flagged for improvement.

## Skill Categories (Baseline)
- Technical: programming languages, frameworks, databases, cloud platforms.
- Tools: CI/CD, version control, ticketing, monitoring.
- Methods: agile/scrum/kanban, testing practices, security practices.
- Soft skills: communication, leadership, collaboration.
- Languages: English/German (or JD-specific requirements).

## JD Alignment Requirements
- Include every required JD skill in the CV (Skills section + evidence).
- Map JD responsibilities to 2-4 Experience bullets.
- Reflect seniority (years or scope) if the JD specifies seniority.

## Output Expectations
- Missing required skills are listed explicitly.
- Skills without evidence are listed with an "add evidence" action.
- Missing sections are listed as blockers.

## References
- `src/core/ats_criteria_extractor.py`
- `src/core/jd_parser.py`
- `src/core/matcher.py`
