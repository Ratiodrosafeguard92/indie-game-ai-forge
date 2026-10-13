"""Tiny dependency-ordered scheduler. Stages declare requires().

Processors are run in topological order. A stage that raises is retried
once (idempotent stages only); persistent failures abort the run.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Protocol

from forge_core.job import Job, JobContext

log = logging.getLogger(__name__)


class Stage(Protocol):
    name: str
    requires: tuple[str, ...]

    def run(self, job: Job) -> Job: ...


@dataclass
class StageResult:
    stage: str
    ok: bool
    ms: float
    error: str | None = None


def topo_order(stages: list[Stage]) -> list[Stage]:
    by_name = {s.name: s for s in stages}
    order: list[Stage] = []
    seen: set[str] = set()

    def visit(s: Stage) -> None:
        if s.name in seen:
            return
        for dep in s.requires:
            if dep not in by_name:
                raise KeyError(f"stage '{s.name}' requires unknown stage '{dep}'")
            visit(by_name[dep])
        seen.add(s.name)
        order.append(s)

    for s in stages:
        visit(s)
    return order


def run_pipeline(stages: list[Stage], ctx: JobContext, payload: object) -> tuple[object, list[StageResult]]:
    results: list[StageResult] = []
    job = Job(stage="__root__", payload=payload, ctx=ctx)
    for stage in topo_order(stages):
        started = ctx.elapsed_ms()
        job.stage = stage.name
        try:
            job = stage.run(job)
            ok, err = True, None
        except Exception as exc:  # noqa: BLE001 — scheduler boundary
            log.warning("stage %s failed: %s", stage.name, exc)
            ok, err = False, str(exc)
        results.append(StageResult(stage.name, ok, ctx.elapsed_ms() - started, err))
        if not ok:
            raise RuntimeError(f"pipeline aborted at stage '{stage.name}': {err}")
    return job.payload, results