"""Stage 0: turn the raw prompt into a skeleton DesignIntent.

Accepts a literal prompt string or a path to a .md/.txt brief.
"""
from __future__ import annotations

from pathlib import Path

from forge_core.job import Job
from forge_models.design_intent import DesignIntent


class PromptIngestHandler:
    name = "ingest.prompt"
    requires: tuple[str, ...] = ()

    def run(self, job: Job) -> Job:
        raw = job.payload
        text = Path(raw).read_text(encoding="utf-8") if _looks_like_path(raw) else str(raw)
        intent = DesignIntent.from_prompt(text)
        job.payload = intent
        return job


def _looks_like_path(raw: object) -> bool:
    if not isinstance(raw, str):
        return False
    p = Path(raw)
    return p.suffix in {".md", ".txt", ".brief"} and p.exists()