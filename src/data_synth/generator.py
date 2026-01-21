from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import random

from src.core.ats_criteria_extractor import ATSCriteriaExtractor
from src.core.jd_parser import JDParser
from src.core.matcher import BaselineMatcher


GENERATOR_VERSION = "1.0.0"
DEFAULT_TAXONOMY_PATH = Path("data/synthetic/skill_taxonomy.json")


@dataclass(frozen=True)
class SyntheticPair:
    pair_id: str
    cv_text: str
    jd_text: str
    ground_truth: dict[str, object]


def load_taxonomy(path: Path) -> dict[str, object]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _build_synonym_lookup(synonyms: dict[str, str]) -> dict[str, list[str]]:
    lookup: dict[str, list[str]] = {}
    for alias, canonical in synonyms.items():
        lookup.setdefault(canonical, []).append(alias)
    return lookup


class SyntheticGenerator:
    def __init__(self, taxonomy: dict[str, object], seed: int = 0) -> None:
        self.taxonomy = taxonomy
        self.rng = random.Random(seed)
        self.synonyms = taxonomy.get("synonyms", {})
        self.synonym_lookup = _build_synonym_lookup(self.synonyms)

    def generate_pair(
        self,
        pair_index: int,
        lang: str,
        job_family: str,
        difficulty: str,
    ) -> SyntheticPair:
        pair_seed = self.rng.randint(0, 10_000_000)
        local_rng = random.Random(pair_seed)
        job_family_name, required, preferred = self._select_job_family(job_family, local_rng)
        edge_cases = self._edge_cases(difficulty, local_rng)
        label, missing_required = self._assign_label(
            required,
            difficulty,
            edge_cases["missing_experience"],
            local_rng,
        )
        cv_skills = self._build_cv_skills(required, preferred, missing_required, label, local_rng)

        cv_text = self._build_cv_text(
            lang=lang,
            cv_skills=cv_skills,
            experience=not edge_cases["missing_experience"],
            education=not edge_cases["missing_education"],
            keyword_stuffing=edge_cases["keyword_stuffing"],
            noisy=edge_cases["noisy_formatting"],
            synonym_only=edge_cases["synonym_only"],
            rng=local_rng,
        )
        jd_text = self._build_jd_text(
            lang=lang,
            required=required,
            preferred=preferred,
            noisy=edge_cases["noisy_formatting"],
        )

        expected_score, matched_skills, missing_required_sorted = self._baseline_expectations(
            cv_text=cv_text,
            jd_text=jd_text,
            required=required,
            preferred=preferred,
        )
        expected_label = label
        expected_score_range = [
            round(expected_score, 2),
            round(expected_score, 2),
        ]

        ground_truth = {
            "expected_label": expected_label,
            "missing_required_skills": missing_required_sorted,
            "matched_skills": matched_skills,
            "expected_score_range": expected_score_range,
            "rationale": self._build_rationale(
                expected_label=expected_label,
                missing_required=missing_required_sorted,
                edge_cases=edge_cases,
            ),
            "metadata": {
                "language": lang,
                "job_family": job_family_name,
                "difficulty": difficulty,
                "seed": pair_seed,
                "generator_version": GENERATOR_VERSION,
            },
        }

        return SyntheticPair(
            pair_id=f"pair_{pair_index:04d}",
            cv_text=cv_text,
            jd_text=jd_text,
            ground_truth=ground_truth,
        )

    def _select_job_family(
        self, job_family: str, rng: random.Random
    ) -> tuple[str, list[str], list[str]]:
        families = self.taxonomy.get("job_families", {})
        if job_family == "mixed":
            job_family = rng.choice(sorted(families.keys()))
        family = families[job_family]
        return job_family, list(family["required"]), list(family["preferred"])

    def _assign_label(
        self,
        required: list[str],
        difficulty: str,
        missing_experience: bool,
        rng: random.Random,
    ) -> tuple[str, list[str]]:
        if difficulty == "mixed":
            difficulty = rng.choice(["easy", "medium", "hard"])
        if difficulty == "easy":
            label = "strong_match"
        elif difficulty == "medium":
            label = rng.choice(["strong_match", "partial_match"])
        else:
            label = rng.choice(["partial_match", "mismatch"])

        if label == "strong_match":
            if missing_experience:
                return "partial_match", rng.sample(required, k=min(1, len(required)))
            return label, []
        if label == "partial_match":
            missing = rng.sample(required, k=min(1, len(required)))
            return label, missing
        missing = list(required)
        return label, missing

    def _build_cv_skills(
        self,
        required: list[str],
        preferred: list[str],
        missing_required: list[str],
        label: str,
        rng: random.Random,
    ) -> list[str]:
        cv_skills = [skill for skill in required if skill not in missing_required]
        if label != "mismatch":
            extras = rng.sample(preferred, k=min(2, len(preferred)))
            cv_skills.extend(extras)
        else:
            other = self._select_other_family(required, rng)
            cv_skills = other
        return sorted(set(cv_skills))

    def _select_other_family(self, required: list[str], rng: random.Random) -> list[str]:
        families = self.taxonomy.get("job_families", {}).values()
        candidates = []
        for family in families:
            skills = list(family["required"])
            if set(skills) != set(required):
                candidates.append(skills)
        return rng.choice(candidates) if candidates else required

    def _edge_cases(self, difficulty: str, rng: random.Random) -> dict[str, bool]:
        if difficulty == "mixed":
            difficulty = rng.choice(["easy", "medium", "hard"])
        if difficulty == "hard":
            return {
                "keyword_stuffing": True,
                "missing_education": rng.choice([True, False]),
                "missing_experience": rng.choice([True, False]),
                "noisy_formatting": True,
                "synonym_only": rng.choice([True, False]),
            }
        if difficulty == "medium":
            return {
                "keyword_stuffing": False,
                "missing_education": rng.choice([True, False]),
                "missing_experience": False,
                "noisy_formatting": rng.choice([True, False]),
                "synonym_only": rng.choice([True, False]),
            }
        return {
            "keyword_stuffing": False,
            "missing_education": False,
            "missing_experience": False,
            "noisy_formatting": False,
            "synonym_only": False,
        }

    def _build_cv_text(
        self,
        lang: str,
        cv_skills: list[str],
        experience: bool,
        education: bool,
        keyword_stuffing: bool,
        noisy: bool,
        synonym_only: bool,
        rng: random.Random,
    ) -> str:
        contact_header = "Contact" if lang == "en" else "Kontakt"
        profile_header = "Profile" if lang == "en" else "Profil"
        experience_header = "Experience" if lang == "en" else "Berufserfahrung"
        education_header = "Education" if lang == "en" else "Ausbildung"
        skills_header = "Skills"
        languages_header = "Languages" if lang == "en" else "Sprachen"

        skill_terms = self._maybe_apply_synonyms(cv_skills, synonym_only, rng)
        skill_lines = self._format_list(skill_terms, noisy)

        content = [
            f"{contact_header}: Jordan Taylor",
            "Email: jordan.taylor@example.com",
            "Location: Berlin",
            "",
            f"{profile_header}:",
            "Detail-oriented engineer focused on reliable delivery.",
            "",
        ]

        if experience:
            content.extend(
                [
                    f"{experience_header}:",
                    "2021-2024 Backend Engineer - Northwind Systems",
                ]
            )
            if not keyword_stuffing:
                content.append("Built services using python and sql.")
            content.append("")

        if education:
            content.extend(
                [
                    f"{education_header}:",
                    "BSc Computer Science",
                    "",
                ]
            )

        content.extend(
            [
                f"{skills_header}:",
                *skill_lines,
                "",
                f"{languages_header}:",
                "English, German",
            ]
        )
        return "\n".join(content).strip() + "\n"

    def _build_jd_text(
        self,
        lang: str,
        required: list[str],
        preferred: list[str],
        noisy: bool,
    ) -> str:
        title = "Backend Engineer" if lang == "en" else "Backend Engineer"
        responsibilities_header = "Responsibilities" if lang == "en" else "Aufgaben"
        requirements_header = "Required" if lang == "en" else "Anforderungen"
        preferred_header = "Preferred" if lang == "en" else "Wuensche"

        required_lines = self._format_list(required, noisy)
        preferred_lines = self._format_list(preferred, noisy)

        content = [
            title,
            "Remote: yes",
            "",
            f"{responsibilities_header}:",
            "- Build reliable services.",
            "- Collaborate with cross-functional teams.",
            "",
            f"{requirements_header}:",
            *required_lines,
            "",
            f"{preferred_header}:",
            *preferred_lines,
        ]
        return "\n".join(content).strip() + "\n"

    def _format_list(self, items: list[str], noisy: bool) -> list[str]:
        if not items:
            return ["- not specified"]
        if noisy:
            return [f"*   {item}" if idx % 2 == 0 else f"-  {item}" for idx, item in enumerate(items)]
        return [f"- {item}" for item in items]

    def _maybe_apply_synonyms(
        self,
        skills: list[str],
        synonym_only: bool,
        rng: random.Random,
    ) -> list[str]:
        if not synonym_only:
            return skills
        replaced = []
        for skill in skills:
            options = self.synonym_lookup.get(skill, [])
            if options:
                replaced.append(rng.choice(options))
            else:
                replaced.append(skill)
        return replaced

    def _baseline_expectations(
        self,
        cv_text: str,
        jd_text: str,
        required: list[str],
        preferred: list[str],
    ) -> tuple[float, list[str], list[str]]:
        cv = ATSCriteriaExtractor().extract(cv_text)
        jd = JDParser().parse(jd_text)
        result = BaselineMatcher().match(cv, jd)
        matched = {skill.lower() for skill in result.breakdown["skills"]["matched"]}
        expected_skills = {skill.lower() for skill in required + preferred}
        matched_skills = sorted(matched & expected_skills)
        missing_required = sorted({skill.lower() for skill in required} - matched)
        return result.score, matched_skills, missing_required

    def _build_rationale(
        self,
        expected_label: str,
        missing_required: list[str],
        edge_cases: dict[str, bool],
    ) -> str:
        parts = [f"label={expected_label}"]
        if missing_required:
            parts.append(f"missing_required={','.join(missing_required)}")
        for key, value in edge_cases.items():
            if value:
                parts.append(key)
        return "; ".join(parts)
