"""GameProject: the final shape handed to output drivers."""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from forge_models.design_intent import DesignIntent, LevelNode


@dataclass
class GameProject:
    title: str
    slug: str
    premise: str
    systems: list[str] = field(default_factory=list)
    levels: list[LevelNode] = field(default_factory=list)
    beats: list[str] = field(default_factory=list)

    @classmethod
    def from_intent(cls, intent: DesignIntent) -> "GameProject":
        title = _title_from(intent.prompt)
        return cls(
            title=title,
            slug=_slugify(title),
            premise=intent.premise or intent.prompt[:120],
            systems=sorted(intent.systems),
            levels=list(intent.levels),
            beats=list(intent.beats),
        )

    def to_manifest(self) -> dict:
        return {
            "title": self.title,
            "slug": self.slug,
            "premise": self.premise,
            "systems": self.systems,
            "beats": self.beats,
            "levels": [l.to_dict() for l in self.levels],
            "generator": "indie-game-ai-forge",
            "version": "0.6.3",
        }


def _title_from(prompt: str) -> str:
    first = prompt.strip().splitlines()[0] if prompt.strip() else "Untitled Forge"
    return first[:48].strip() or "Untitled Forge"


def _slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "untitled"