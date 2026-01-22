from __future__ import annotations

from datetime import datetime
from pathlib import Path

from src.core.ats_criteria_extractor import ATSCriteria
from src.core.jd_parser import JDParseResult
from src.core.matcher import MatchResult


def build_report_payload(
    match: MatchResult,
    ats: ATSCriteria,
    jd: JDParseResult,
    strategy: str,
    dataset_id: str | None = None,
    prompt_chain: dict[str, object] | None = None,
) -> dict[str, object]:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    breakdown = match.breakdown
    penalties = breakdown.get("penalties", {})
    skills = []
    for group, values in ats.skills.items():
        if values:
            skills.append({"group": group, "values": values})

    matched = breakdown.get("skills", {}).get("matched", []) or breakdown.get("top_matched_skills", [])
    gaps = breakdown.get("skills", {}).get("gaps", [])
    evidence = breakdown.get("evidence_snippets", {})

    return {
        "meta": {
            "timestamp": timestamp,
            "strategy": strategy,
            "dataset_id": dataset_id or "n/a",
            "candidate_name": ats.contact.get("name", "not_found"),
            "jd_role": jd.role,
        },
        "summary": {
            "score": match.score,
            "verdict": "strong_match"
            if match.score >= 80
            else "partial_match"
            if match.score >= 60
            else "mismatch",
        },
        "score_breakdown": breakdown,
        "skills": skills,
        "matched_skills": matched,
        "missing_required": penalties.get("missing_required_skills", []),
        "evidence_snippets": evidence,
        "warnings": {
            "missing_fields": ats.missing_fields,
            "keyword_stuffing_risk": penalties.get("keyword_stuffing_risk"),
        },
        "prompt_chain": prompt_chain or {},
    }


def render_report_markdown(payload: dict[str, object]) -> str:
    meta = payload.get("meta", {})
    summary = payload.get("summary", {})
    breakdown = payload.get("score_breakdown", {})
    lines = [
        "# ATS CV Scorer - Match Report",
        "",
        "## Meta",
        f"- timestamp: {meta.get('timestamp')}",
        f"- strategy: {meta.get('strategy')}",
        f"- dataset_id: {meta.get('dataset_id')}",
        f"- candidate_name: {meta.get('candidate_name')}",
        f"- jd_role: {meta.get('jd_role')}",
        "",
        "## Executive Summary",
        f"- score: {summary.get('score')}",
        f"- verdict: {summary.get('verdict')}",
        "",
        "## Score Breakdown",
        f"- skills: {breakdown.get('skills')}",
        f"- experience: {breakdown.get('experience')}",
        f"- education: {breakdown.get('education')}",
        f"- language: {breakdown.get('language')}",
        f"- location: {breakdown.get('location')}",
        f"- semantic_similarity: {breakdown.get('semantic_similarity')}",
        f"- skill_overlap_score: {breakdown.get('skill_overlap_score')}",
        f"- section_coverage: {breakdown.get('section_coverage')}",
        f"- penalties: {breakdown.get('penalties')}",
        "",
        "## Matched Skills + Evidence",
    ]
    for skill in payload.get("matched_skills", []):
        evidence = payload.get("evidence_snippets", {}).get(skill, "no_evidence")
        lines.append(f"- {skill}: {evidence}")
    lines.extend(
        [
            "",
            "## Missing Required + Suggestions",
            f"- missing_required: {payload.get('missing_required')}",
            "",
            "## Parsing Notes / Warnings",
            f"- missing_fields: {payload.get('warnings', {}).get('missing_fields')}",
            f"- keyword_stuffing_risk: {payload.get('warnings', {}).get('keyword_stuffing_risk')}",
        ]
    )
    chain = payload.get("prompt_chain") or {}
    if chain:
        lines.extend(
            [
                "",
                "## Prompt Chain Results",
                f"- strategy: {chain.get('strategy')}",
                f"- run_id: {chain.get('chain_run_id')}",
            ]
        )
    return "\n".join(lines)


def write_report_json(payload: dict[str, object], path: Path) -> None:
    path.write_text(json_dumps(payload), encoding="utf-8")


def write_report_markdown(payload: dict[str, object], path: Path) -> None:
    path.write_text(render_report_markdown(payload), encoding="utf-8")


def json_dumps(payload: dict[str, object]) -> str:
    import json

    return json.dumps(payload, indent=2)
