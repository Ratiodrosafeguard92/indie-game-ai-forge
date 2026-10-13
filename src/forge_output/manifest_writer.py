"""Stage 6: assemble a GameProject from the DesignIntent."""
from __future__ import annotations

from forge_core.job import Job
from forge_models.design_intent import DesignIntent
from forge_models.game_project import GameProject


class ManifestWriter:
    name = "output.manifest"
    requires = ("process.balance",)

    def run(self, job: Job) -> Job:
        intent: DesignIntent = job.payload
        project = GameProject.from_intent(intent)
        job.ctx.scratch["project"] = project
        return job