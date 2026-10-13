"""Stage 4: stamp a lightweight narrative frame (premise, beats, NPC seeds)."""
from __future__ import annotations

import random

from forge_core.job import Job
from forge_models.design_intent import DesignIntent


class NarrativeProcessor:
    name = "process.narrative"
    requires = ("process.levels",)

    def run(self, job: Job) -> Job:
        intent: DesignIntent = job.payload
        rng = random.Random((job.ctx.seed or 0) ^ 0xF0F0)
        premise = intent.prompt.strip().splitlines()[0] if intent.prompt.strip() else "an unnamed world"
        intent.premise = premise
        intent.beats = [f"Beat {i}: {_beat(rng)}" for i in range(1, len(intent.levels) + 1)]
        return job


def _beat(rng: random.Random) -> str:
    return rng.choice([
        "the player arrives and the rules are wrong",
        "an ally is not what they seem",
        "the cost of progress is named out loud",
        "the world answers back",
        "the final door is already open",
    ])