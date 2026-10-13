"""IngestHandler base + RawSource."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from forge_models.design_intent import DesignIntent


@dataclass
class RawSource:
    kind: str  # "prompt" | "reference" | "asset" | "config"
    text: str = ""
    path: Path | None = None


class IngestHandler(Protocol):
    name: str
    requires: tuple[str, ...]

    def accepts(self, source: RawSource) -> bool: ...
    def ingest(self, source: RawSource) -> DesignIntent: ...