"""Stage 2: pick core systems (combat, movement, inventory, save) from tags."""
from __future__ import annotations

from forge_core.job import Job
from forge_models.design_intent import DesignIntent

SYSTEM_TAGS = {
    "combat": "CombatSystem",
    "shooter": "ProjectileSystem",
    "rpg": "StatsSystem",
    "platformer": "PlatformerController",
    "puzzle": "GridPuzzleSystem",
    "horror": "SanitySystem",
    "survival": "HungerSystem",
    "inventory": "InventorySystem",
}


class SystemsProcessor:
    name = "process.systems"
    requires = ("ingest.reference",)

    def run(self, job: Job) -> Job:
        intent: DesignIntent = job.payload
        for tag in intent.tags:
            if tag in SYSTEM_TAGS:
                intent.systems.add(SYSTEM_TAGS[tag])
        if not intent.systems:
            intent.systems.add("CoreLoopSystem")
        return job