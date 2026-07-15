# AI Lecture Note Taker

[![tests](https://github.com/shauryamalhotra957-wq/ai-lecture-note-taker/actions/workflows/tests.yml/badge.svg)](https://github.com/shauryamalhotra957-wq/ai-lecture-note-taker/actions/workflows/tests.yml)

Upload a lecture recording or transcript and get clean notes, key concepts, quiz questions, and a study guide.

Tech stack: Python, FastAPI, OpenAI Whisper-compatible transcription API.

## Project Snapshot

| Area | Detail |
| --- | --- |
| Experience | Study-pack generator for lecture recordings or transcripts |
| Core system | Transcript cleanup, notes, concepts, quiz questions, study guides, exports |
| Design signal | Simple upload-to-results flow with deterministic demo mode |
| Quality signal | Pytest CI on Python 3.11 and 3.12 |

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\scripts\run.ps1
```

Open http://127.0.0.1:8009

## OpenAI Setup

The app runs in demo mode without secrets. For real transcription:

```powershell
Copy-Item .env.example .env
notepad .env
```

Set:

```text
OPENAI_API_KEY=sk-...
OPENAI_TRANSCRIBE_MODEL=whisper-1
```

You can upload `.txt`, `.md`, `.srt`, or `.vtt` files as transcript demos, or audio/video files for transcription.

## Features

- Recording/transcript upload
- OpenAI transcription path with deterministic demo fallback
- Clean transcript generation
- Summary bullets
- Detailed notes
- Key concepts with evidence
- Quiz questions with answers
- Study guide and flashcards
- Markdown and JSON downloads
- Automatic long-audio chunking for API upload limits

## API

- `GET /api/health`
- `POST /api/analyze`
- `GET /api/results/{job_id}.md`
- `GET /api/results/{job_id}.json`

## Test

```powershell
.\.venv\Scripts\python.exe -m pytest
```

GitHub Actions runs the same pytest suite on Python 3.11 and 3.12 for pushes and pull requests.

## Sample

Use `sample_assets/lecture-transcript.txt` for an instant demo.

## Experience Design

The study workspace follows the [Lecture Note Taker design system](design-system/ai-lecture-note-taker/MASTER.md), using calm contrast, explicit processing states, accessible controls, responsive reading surfaces, and reduced-motion behavior.

