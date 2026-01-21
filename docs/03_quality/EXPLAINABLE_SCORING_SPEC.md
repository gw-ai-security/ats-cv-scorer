# Explainable Scoring Specification

## Purpose
Define the current, explainable scoring logic for the ATS CV Scorer and document what is and is not implemented.

## Scope
- Applies to the rule-based baseline matcher and the hybrid ML matcher.
- Describes score components, weights, and output schema expectations.

## Baseline Matcher (Deterministic)

### Inputs
- CV criteria extracted by `src/core/ats_criteria_extractor.py`
- JD parse result from `src/core/jd_parser.py`

### Score Components and Weights
Total score is a weighted sum, scaled to 0–100:
```
total = (
  skills_score * 0.50 +
  experience_score * 0.20 +
  education_score * 0.15 +
  language_score * 0.10 +
  location_score * 0.05
)
score = round(total * 100, 2)
```

### Component Definitions
- **skills_score**
  - CV skills: all skills from CV sections + certifications + languages.
  - JD skills: `jd.skills` + `jd.keywords` (keywords include tokens from responsibilities).
  - `skills_score = len(matched) / len(jd_skills)` (or 1.0 if no JD skills).
  - Output: `matched`, `gaps`, `score`.
- **experience_score**
  - If no seniority requirement found: score = 1.0.
  - Else: score = 1.0 if CV has experience entries, else 0.0.
- **education_score**
  - If JD does not mention bachelor/master/phd: score = 1.0.
  - Else: score = 1.0 if CV has education entries, else 0.0.
- **language_score**
  - Only considers `german` and `english` as explicit JD language requirements.
  - Score = matched languages / required languages (or 1.0 if none).
- **location_score**
  - If remote role: score = 1.0.
  - If no JD location requirement: score = 1.0.
  - Else: score = 1.0 if JD location is contained in CV location, else 0.0.

### Penalties (Informational Only)
- **missing_required_skills**: currently derived from `jd.skills + jd.keywords` minus CV skills.
- **keyword_stuffing_risk**: true if skills are present but CV experience section is empty.
- These penalties are surfaced for explainability only and do not change scores yet.

### Baseline Output Schema
```
{
  "score": float,
  "breakdown": {
    "skills": {"matched": [...], "gaps": [...], "score": float},
    "experience": {..., "score": float},
    "education": {..., "score": float},
    "language": {..., "score": float},
    "location": {..., "score": float},
    "penalties": {
      "missing_required_skills": [...],
      "missing_required_count": int,
      "keyword_stuffing_risk": bool
    }
  }
}
```

### Known Limitations (Baseline)
- JD keyword extraction pulls tokens from responsibilities (e.g., "build", "collaborate"),
  which inflates skill gaps and lowers `skills_score`.
- No penalties for keyword stuffing or missing evidence beyond section presence.
- Synonym handling only uses the hard-coded skill extractor synonyms; no semantic expansion.

## Hybrid ML Matcher (Optional)

### Inputs
- Same CV/JD criteria as baseline, plus raw CV/JD text for semantic similarity.

### Feature Fusion Weights
```
total = (
  semantic_similarity * 0.60 +
  skill_overlap_score * 0.25 +
  section_coverage * 0.15
)
score = round(total * 100, 2)
```

### Components
- **semantic_similarity**: cosine similarity of embeddings (default model).
- **skill_overlap_score**: overlap of CV vs JD skills/keywords.
- **section_coverage**: fraction of present sections (summary, experience, education, skills, languages).

### Hybrid Output Schema
```
{
  "score": float,
  "breakdown": {
    "semantic_similarity": float,
    "skill_overlap_score": float,
    "section_coverage": float,
    "top_matched_skills": [...],
    "top_matched_chunks": [...],
    "penalties": {
      "missing_required_skills": [...],
      "missing_required_count": int,
      "keyword_stuffing_risk": bool
    }
  }
}
```

### Calibration
- Optional calibrator (`ML_CALIBRATOR_PATH`) can rescale final scores.
- If not configured, raw fusion score is used.

## TODO (Not Implemented Yet)
- Keyword stuffing penalty applied to score (currently informational only).
- Missing required skill penalties beyond skill overlap ratio.
- Synonym-only credit beyond deterministic synonym lists.

## Worked Examples (Synthetic)
### Example A: pair_0002 (Synthetic, EN)
Baseline breakdown:
```
skills_score = 0.4167
experience_score = 1.0 (no seniority requirement)
education_score = 1.0 (no degree requirement)
language_score = 1.0 (no language requirement)
location_score = 1.0 (remote role)
```
Score:
```
total = 0.50*0.4167 + 0.20*1 + 0.15*1 + 0.10*1 + 0.05*1 = 0.7083
score = 70.83
```
Matched skills: `communication, numpy, pandas, python, sql`  
Gaps include JD keywords from responsibilities (e.g., `build`, `collaborate`).

### Example B: pair_0008 (Synthetic, EN)
Baseline breakdown:
```
skills_score = 0.3636
experience_score = 1.0 (no seniority requirement)
education_score = 1.0 (no degree requirement)
language_score = 1.0 (no language requirement)
location_score = 1.0 (remote role)
```
Score:
```
total = 0.50*0.3636 + 0.20*1 + 0.15*1 + 0.10*1 + 0.05*1 = 0.6818
score = 68.18
```
Matched skills: `communication, leadership, python, sql`  
Gaps include JD keywords from responsibilities.

## References
- `src/core/matcher.py`
- `src/core/ml/feature_fusion.py`
- `docs/04_evaluation/EVALUATION_RESULTS.md`
