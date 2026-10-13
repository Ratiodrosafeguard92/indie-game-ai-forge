"""Job + JobContext: the unit of work the scheduler shuffles around."""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass
class JobContext:
    job_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    seed: int = 0
    started_at: float = field(default_factory=time.time)
    scratch: dict[str, Any] = field(default_factory=dict)

    def elapsed_ms(self) -> float:
        return (time.time() - self.started_at) * 1000.0


@dataclass
class Job:
    stage: str
    payload: Any
    ctx: JobContext

    def tag(self) -> str:
        return f"{self.ctx.job_id}:{self.stage}"