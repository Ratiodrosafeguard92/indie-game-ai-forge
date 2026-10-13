"""Default pipeline assembly. Wires ingest → processors → output."""
from __future__ import annotations

from forge_cli.bootstrap import ForgeEnv
from forge_core.job import JobContext
from forge_core.pipeline import Pipeline
from forge_ingest.prompt_handler import PromptIngestHandler
from forge_ingest.reference_handler import ReferenceIngestHandler
from forge_output.driver_godot import GodotDriver
from forge_output.manifest_writer import ManifestWriter
from forge_processors.balance import BalanceProcessor
from forge_processors.levels import LevelProcessor
from forge_processors.narrative import NarrativeProcessor
from forge_processors.systems import SystemsProcessor


def build_default_pipeline(
    env: ForgeEnv,
    target: str = "godot",
    seed: int | None = None,
) -> Pipeline:
    ctx = JobContext(seed=seed or 0)
    ctx.scratch["env"] = env
    ctx.scratch["target"] = target

    drivers = {"godot": GodotDriver}
    driver_cls = drivers.get(target, GodotDriver)

    stages = [
        PromptIngestHandler(),
        ReferenceIngestHandler(),
        SystemsProcessor(),
        LevelProcessor(),
        NarrativeProcessor(),
        BalanceProcessor(),
        ManifestWriter(),
        driver_cls(),
    ]
    return Pipeline(stages, ctx)