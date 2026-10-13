"""Stage 5: rough numeric balance pass over levels + systems."""
from __future__ import annotations

from forge_core.job import Job
from forge_models.design_intent import DesignIntent


class BalanceProcessor:
    name = "process.balance"
    requires = ("process.narrative",)

    def run(self, job: Job) -> Job:
        intent: DesignIntent = job.payload
        n = max(1, len(intent.levels))
        for i, lvl in enumerate(intent.levels):
            lvl.difficulty = round(1.0 + (i / n) * 2.0, 2)
        intent.balance_notes = (
            f"{n} levels, difficulty ramp 1.0→3.0, "
            f"{len(intent.systems)} systems, seed={job.ctx.seed}"
        )
        return job