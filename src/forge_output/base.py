"""OutputDriver base."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from forge_models.game_project import GameProject


@dataclass
class EmitReport:
    driver: str
    files_written: int
    dest: Path


class OutputDriver(Protocol):
    name: str
    requires: tuple[str, ...]

    def emit(self, project: GameProject, dest: Path) -> EmitReport: ...