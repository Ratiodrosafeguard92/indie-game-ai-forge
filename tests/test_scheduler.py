from __future__ import annotations

import pytest

from forge_core.job import JobContext
from forge_core.scheduler import run_pipeline, topo_order


class _Stage:
    def __init__(self, name, requires=(), fn=None):
        self.name = name
        self.requires = tuple(requires)
        self._fn = fn or (lambda job: job)

    def run(self, job):
        return self._fn(job)


def test_topo_order_respects_deps():
    a = _Stage("a")
    b = _Stage("b", requires=("a",))
    c = _Stage("c", requires=("b",))
    assert [s.name for s in topo_order([c, b, a])] == ["a", "b", "c"]


def test_unknown_dep_raises():
    with pytest.raises(KeyError):
        topo_order([_Stage("x", requires=("missing",))])


def test_run_pipeline_threads_payload():
    stages = [
        _Stage("a", fn=lambda j: (setattr(j, "payload", j.payload + 1) or j)),
        _Stage("b", requires=("a",), fn=lambda j: (setattr(j, "payload", j.payload * 10) or j)),
    ]
    out, results = run_pipeline(stages, JobContext(seed=1), 4)
    assert out == 50
    assert all(r.ok for r in results)


def test_stage_failure_aborts():
    def boom(job):
        raise ValueError("nope")

    stages = [_Stage("a", fn=boom)]
    with pytest.raises(RuntimeError, match="pipeline aborted"):
        run_pipeline(stages, JobContext(), "x")