"""Stage 3: generate level graph (rooms/areas + connections)."""
from __future__ import annotations

import random

from forge_core.job import Job
from forge_models.design_intent import DesignIntent, LevelNode


class LevelProcessor:
    name = "process.levels"
    requires = ("process.systems",)

    def run(self, job: Job) -> Job:
        intent: DesignIntent = job.payload
        rng = random.Random(job.ctx.seed or 6767)
        count = max(3, min(12, len(intent.tags) + 3))
        nodes = [LevelNode(id=f"L{i:02d}", name=_name(rng), kind=_kind(rng)) for i in range(count)]
        for i in range(1, count):
            nodes[i].connects_to.append(nodes[i - 1].id)
            if rng.random() < 0.4 and i > 2:
                nodes[i].connects_to.append(nodes[rng.randrange(i - 1)].id)
        intent.levels = nodes
        return job


def _name(rng: random.Random) -> str:
    adj = ["Hollow", "Ashen", "Verdant", "Rusted", "Pale", "Sunken", "Glass"]
    noun = ["Reach", "Vault", "Hollow", "Spire", "Marsh", "Terminal", "Garden"]
    return f"{rng.choice(adj)} {rng.choice(noun)}"


def _kind(rng: random.Random) -> str:
    return rng.choice(["hub", "combat", "puzzle", "boss", "connector"])