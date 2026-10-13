"""Stage 1: fold reference material (genre notes, mood boards) into intent."""
from __future__ import annotations

from forge_core.job import Job
from forge_models.design_intent import DesignIntent


class ReferenceIngestHandler:
    name = "ingest.reference"
    requires = ("ingest.prompt",)

    def run(self, job: Job) -> Job:
        intent: DesignIntent = job.payload
        # Reference text is optional; the scheduler passes it via scratch.
        ref = job.ctx.scratch.get("reference_text")
        if ref:
            intent.references.append(str(ref))
            intent.tags.update(_tags_from(ref))
        return job


def _tags_from(text: str) -> set[str]:
    stop = {"the", "a", "an", "of", "and", "to", "in", "with"}
    return {w.lower() for w in text.split() if w.lower() not in stop and len(w) > 3}