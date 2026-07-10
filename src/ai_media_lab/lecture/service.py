from __future__ import annotations

from pathlib import Path

from fastapi import UploadFile
from pydantic import ValidationError

from ai_media_lab.common.config import service_path
from ai_media_lab.common.files import new_job_id, save_upload, write_json
from ai_media_lab.common.openai_service import generate_json_with_openai, transcribe_media
from ai_media_lab.common.schemas import LectureAnalysis, LectureJobResult
from ai_media_lab.common.text_analysis import analyze_lecture_text


LECTURE_AI_INSTRUCTIONS = """
You create concise, accurate study material from a lecture transcript.
Return only JSON matching these keys:
title, clean_transcript, summary, clean_notes, key_concepts, quiz_questions, study_guide.
key_concepts items need concept, why_it_matters, evidence.
quiz_questions items need question, options, answer, explanation.
study_guide needs focus_areas, review_plan, flashcards, exam_tips.
flashcards items need front and back.
Do not invent facts that are not supported by the transcript.
"""


def render_lecture_markdown(result: LectureJobResult) -> str:
    analysis = result.analysis
    lines = [
        analysis.clean_notes.rstrip(),
        "",
        "## Quiz",
    ]
    for index, question in enumerate(analysis.quiz_questions, start=1):
        lines.append(f"{index}. {question.question}")
        for option in question.options:
            marker = "*" if option == question.answer else "-"
            lines.append(f"   {marker} {option}")
        lines.append(f"   Answer: {question.answer}")
        lines.append(f"   Why: {question.explanation}")
        lines.append("")

    lines.extend(["## Study Guide", "### Focus Areas"])
    lines.extend(f"- {item}" for item in analysis.study_guide.focus_areas)
    lines.extend(["", "### Review Plan"])
    lines.extend(f"- {item}" for item in analysis.study_guide.review_plan)
    lines.extend(["", "### Flashcards"])
    for card in analysis.study_guide.flashcards:
        lines.append(f"- **{card.front}** {card.back}")
    lines.extend(["", "## Transcript", analysis.clean_transcript])
    return "\n".join(lines).strip() + "\n"


def _maybe_ai_enrich(base: LectureAnalysis) -> LectureAnalysis:
    payload = base.model_dump(mode="json")
    ai_payload = generate_json_with_openai(LECTURE_AI_INSTRUCTIONS, payload)
    if not ai_payload:
        return base
    try:
        return LectureAnalysis.model_validate(ai_payload)
    except ValidationError:
        return base


async def process_lecture_upload(upload: UploadFile, topic: str | None, demo_mode: bool = False) -> LectureJobResult:
    job_id = new_job_id("lecture")
    upload_path = await save_upload(upload, service_path("lecture", "uploads"))
    transcript = transcribe_media(upload_path, kind="lecture", prefer_segments=False, force_demo=demo_mode)
    base_analysis = analyze_lecture_text(transcript.text, topic=topic)
    analysis = base_analysis if demo_mode else _maybe_ai_enrich(base_analysis)

    result = LectureJobResult(
        job_id=job_id,
        filename=upload.filename or upload_path.name,
        transcript=transcript,
        analysis=analysis,
        markdown_url=f"/api/results/{job_id}.md",
        json_url=f"/api/results/{job_id}.json",
    )

    result_dir = service_path("lecture", "results")
    write_json(result_dir / f"{job_id}.json", result.model_dump(mode="json"))
    (result_dir / f"{job_id}.md").write_text(render_lecture_markdown(result), encoding="utf-8")
    return result


def result_file(job_id: str, extension: str) -> Path:
    filename = f"{job_id}.{extension.lstrip('.')}"
    return service_path("lecture", "results") / filename

