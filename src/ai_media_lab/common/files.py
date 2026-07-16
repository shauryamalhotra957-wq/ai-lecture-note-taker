from __future__ import annotations

import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


SAFE_NAME_RE = re.compile(r"[^A-Za-z0-9._-]+")


class UploadTooLargeError(ValueError):
    def __init__(self, max_bytes: int) -> None:
        self.max_bytes = max_bytes
        super().__init__(f"Upload exceeds the {max_bytes}-byte limit")


def safe_filename(filename: str | None, fallback: str = "upload.bin") -> str:
    name = Path(filename or fallback).name.strip() or fallback
    cleaned = SAFE_NAME_RE.sub("-", name).strip(".-")
    return cleaned or fallback


def new_job_id(prefix: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"{prefix}-{stamp}-{uuid4().hex[:8]}"


async def save_upload(upload: UploadFile, destination_dir: Path, max_bytes: int | None = None) -> Path:
    destination_dir.mkdir(parents=True, exist_ok=True)
    filename = safe_filename(upload.filename)
    path = destination_dir / f"{uuid4().hex}-{filename}"
    bytes_written = 0
    try:
        with path.open("wb") as output:
            while True:
                chunk = await upload.read(1024 * 1024)
                if not chunk:
                    break
                bytes_written += len(chunk)
                if max_bytes is not None and bytes_written > max_bytes:
                    raise UploadTooLargeError(max_bytes)
                output.write(chunk)
    except Exception:
        path.unlink(missing_ok=True)
        raise
    await upload.seek(0)
    return path


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)


def read_text(path: Path, max_chars: int = 300_000) -> str:
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        return handle.read(max_chars)


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)

