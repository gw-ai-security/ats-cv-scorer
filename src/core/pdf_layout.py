from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Iterable

from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from src.core.ats_criteria_extractor import ATSCriteria
from src.core.jd_parser import JDParseResult
from src.core.matcher import MatchResult
from src.core.report_export import build_report_payload


def _draw_section_header(pdf: canvas.Canvas, title: str, y: float) -> float:
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(72, y, title)
    return y - 18


def _draw_lines(pdf: canvas.Canvas, lines: Iterable[str], y: float) -> float:
    pdf.setFont("Helvetica", 10)
    for line in lines:
        if y < 72:
            pdf.showPage()
            y = letter[1] - 72
            pdf.setFont("Helvetica", 10)
        pdf.drawString(72, y, line[:120])
        y -= 14
    return y


def _render_template_lines(context: dict[str, object]) -> list[str] | None:
    templates_dir = BytesIO  # sentinel for type hints
    try:
        templates_dir = (Path(__file__).parent / "templates").resolve()
        env = Environment(loader=FileSystemLoader(str(templates_dir)), autoescape=False)
        template = env.get_template("score_report.txt.j2")
        text = template.render(**context)
        return [line.rstrip() for line in text.splitlines() if line.strip()]
    except TemplateNotFound:
        return None


def render_score_report_pdf(
    match: MatchResult,
    ats: ATSCriteria,
    jd: JDParseResult,
    strategy: str,
    dataset_id: str | None = None,
    prompt_chain: dict[str, object] | None = None,
) -> bytes:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 72

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(72, y, "ATS CV Scorer - Match Report")
    y -= 24

    payload = build_report_payload(
        match=match,
        ats=ats,
        jd=jd,
        strategy=strategy,
        dataset_id=dataset_id,
        prompt_chain=prompt_chain,
    )
    breakdown = payload["score_breakdown"]
    component_lines = [
        f"skills: {breakdown.get('skills')}",
        f"experience: {breakdown.get('experience')}",
        f"education: {breakdown.get('education')}",
        f"language: {breakdown.get('language')}",
        f"location: {breakdown.get('location')}",
        f"semantic_similarity: {breakdown.get('semantic_similarity')}",
        f"skill_overlap_score: {breakdown.get('skill_overlap_score')}",
        f"section_coverage: {breakdown.get('section_coverage')}",
        f"penalties: {breakdown.get('penalties')}",
    ]
    matched_lines = []
    for skill in payload.get("matched_skills", []):
        snippet = payload.get("evidence_snippets", {}).get(skill, "no_evidence")
        matched_lines.append(f"{skill}: {snippet}")
    missing_lines = []
    missing_required = payload.get("missing_required", [])
    if missing_required:
        missing_lines.append(f"Missing required: {', '.join(missing_required)}")
    warning_lines = [
        f"missing_fields: {payload.get('warnings', {}).get('missing_fields')}",
        f"keyword_stuffing_risk: {payload.get('warnings', {}).get('keyword_stuffing_risk')}",
    ]

    chain = payload.get("prompt_chain") or {}
    prompt_chain_lines = []
    if chain:
        prompt_chain_lines.append(f"Strategy: {chain.get('strategy')}")
        prompt_chain_lines.append(f"Run ID: {chain.get('chain_run_id')}")
        step1 = chain.get("step_results", {}).get("step1", {})
        if step1:
            prompt_chain_lines.append(
                f"Step1 score: {step1.get('score_0_100')} missing: {', '.join(step1.get('missing_keywords', []))}"
            )
    context = {
        "timestamp": payload["meta"]["timestamp"],
        "strategy": payload["meta"]["strategy"],
        "dataset_id": payload["meta"]["dataset_id"],
        "score": payload["summary"]["score"],
        "verdict": payload["summary"]["verdict"],
        "candidate_name": payload["meta"]["candidate_name"],
        "jd_role": payload["meta"]["jd_role"],
        "component_lines": [line for line in component_lines if line],
        "matched_lines": matched_lines or ["No matched skills recorded."],
        "missing_lines": missing_lines or ["No missing required skills flagged."],
        "warning_lines": warning_lines,
        "prompt_chain_lines": prompt_chain_lines,
    }
    template_lines = _render_template_lines(context)
    if template_lines:
        y = _draw_lines(pdf, template_lines, y - 4)
    else:
        y = _draw_section_header(pdf, "Meta Info", y)
        meta_lines = [
            f"Strategy: {strategy}",
            f"Score: {match.score}%",
            f"Candidate: {ats.contact.get('name', 'not_found')}",
            f"JD Role: {jd.role}",
            f"Language(s): {', '.join(ats.languages) if ats.languages else 'not_found'}",
        ]
        y = _draw_lines(pdf, meta_lines, y - 4)
        y = _draw_section_header(pdf, "Extracted Skills", y - 8)
        y = _draw_lines(pdf, skills or ["No skills extracted."], y - 4)
        y = _draw_section_header(pdf, "Score Components", y - 8)
        y = _draw_lines(pdf, component_lines or ["No component breakdown available."], y - 4)
        y = _draw_section_header(pdf, "Top Matches / Deficiencies", y - 8)
        y = _draw_lines(pdf, top_lines, y - 4)

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer.read()
