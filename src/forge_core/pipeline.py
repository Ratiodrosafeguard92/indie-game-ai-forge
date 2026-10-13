"""Pipeline facade: assembles stages, runs them, produces a RunReport."""
from __future__ import annotations

from dataclasses import dataclass

from forge_core.job import JobContext
from forge_core.scheduler import Stage, StageResult, run_pipeline
from forge_models.design_intent import DesignIntent


@dataclass
class RunReport:
    stages: list[StageResult]
    intent: DesignIntent | None = None

    def summary(self) -> str:
        lines = [f"forge run — {len(self.stages)} stages"]
        for r in self.stages:
            mark = "ok " if r.ok else "ERR"
            lines.append(f"  [{mark}] {r.stage:<22} {r.ms:7.1f} ms")
        return "\n".join(lines)


class Pipeline:
    def __init__(self, stages: list[Stage], ctx: JobContext) -> None:
        self._stages = stages
        self._ctx = ctx

    @staticmethod
    def default_stage_names() -> list[str]:
        return [
            "ingest.prompt",
            "ingest.reference",
            "process.systems",
            "process.levels",
            "process.narrative",
            "process.balance",
            "output.manifest",
            "output.driver",
        ]

    def run(self, prompt: str) -> RunReport:
        payload, results = run_pipeline(self._stages, self._ctx, prompt)
        intent = payload if isinstance(payload, DesignIntent) else None
        return RunReport(stages=results, intent=intent)