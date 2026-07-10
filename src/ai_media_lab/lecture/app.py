from __future__ import annotations

from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from ai_media_lab.lecture.service import process_lecture_upload, result_file


STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(
    title="AI Lecture Note Taker",
    description="Upload a lecture recording or transcript and generate notes, concepts, quiz questions, and a study guide.",
    version="0.1.0",
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "app": "lecture-note-taker"}


@app.post("/api/analyze")
async def analyze(
    file: Annotated[UploadFile, File(...)],
    topic: Annotated[str | None, Form()] = None,
    demo_mode: Annotated[bool, Form()] = False,
):
    return await process_lecture_upload(file, topic=topic, demo_mode=demo_mode)


@app.get("/api/results/{artifact}")
def download_result(artifact: str) -> FileResponse:
    if "." not in artifact:
        raise HTTPException(status_code=404, detail="Result not found")
    job_id, extension = artifact.rsplit(".", 1)
    if extension not in {"json", "md"} or not job_id.startswith("lecture-"):
        raise HTTPException(status_code=404, detail="Result not found")
    path = result_file(job_id, extension)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Result not found")
    media_type = "application/json" if extension == "json" else "text/markdown"
    return FileResponse(path, media_type=media_type, filename=path.name)

