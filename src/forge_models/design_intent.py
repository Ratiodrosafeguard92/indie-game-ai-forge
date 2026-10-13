"""DesignIntent: the intermediate the pipeline threads through every stage."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class LevelNode:
    id: str
    name: str
    kind: str
    difficulty: float = 1.0
    connects_to: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "kind": self.kind,
            "difficulty": self.difficulty,
            "connects_to": list(self.connects_to),
        }


@dataclass
class DesignIntent:
    prompt: str
    references: list[str] = field(default_factory=list)
    tags: set[str] = field(default_factory=set)
    systems: set[str] = field(default_factory=set)
    levels: list[LevelNode] = field(default_factory=list)
    premise: str = ""
    beats: list[str] = field(default_factory=list)
    balance_notes: str = ""

    @classmethod
    def from_prompt(cls, text: str) -> "DesignIntent":
        tags = {w.strip(".,:;!?").lower() for w in text.split() if len(w) > 3}
        return cls(prompt=text, tags=tags)