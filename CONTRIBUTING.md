# Contributing to indie-game-ai-forge

Thanks for wanting to help build the AI full indie game generator. This repo is a **pipeline/worker** codebase: ingest handlers pull raw design intent in, processors run the generation stages, output drivers write a playable project out.

## Repo layout

- `src/forge_cli/` — entry / bootstrap (CLI, env loading, run orchestration)
- `src/forge_core/` — core pipeline logic (stage graph, job utils, schedulers)
- `src/forge_ingest/` — ingest handlers (prompt, reference, asset, config)
- `src/forge_processors/` — generation processors (systems, levels, narrative, balance)
- `src/forge_output/` — output drivers (godot, unity, custom igpack, manifest)
- `src/forge_models/` — data models / config schemas
- `src/forge_utils/` — logging, hashing, timing, fs helpers
- `native/forge_native/` — optional C++ accelerator bridge (kept behind a flag)
- `tests/` — pytest suite

## Dev setup

```bash
python -m venv .venv
. .venv/Scripts/activate   # Windows
pip install -e ".[dev]"
pytest -q
```

## Adding an ingest handler

1. Subclass `forge_ingest.base.IngestHandler`.
2. Implement `accepts(source: RawSource) -> bool` and `ingest(source: RawSource) -> DesignIntent`.
3. Register in `forge_ingest.registry.HANDLERS`.
4. Add a test in `tests/test_ingest.py`.

## Adding a processor

Processors are pure-ish: take a `DesignIntent` plus a `JobContext`, return a mutated `DesignIntent` or a `ProcessorResult`. Keep them idempotent where possible so the scheduler can retry.

## Adding an output driver

Subclass `forge_output.base.OutputDriver`, implement `emit(project: GameProject, dest: Path) -> EmitReport`. Drivers must be safe to run against a directory that already exists (overwrite only files they own).

## Style

- `ruff` + `black`, line length 100.
- Type hints required on public functions.
- No network calls inside processors; do I/O at the edges (ingest/output).

## PR checklist

- [ ] tests pass (`pytest -q`)
- [ ] `ruff check src tests`
- [ ] new processor/handler/driver has at least one test
- [ ] no new hard dependency without a note in `pyproject.toml`

## Community

This is a hobbyist/educational project. Cheat-adjacent, mod, and exploit-research forks are welcome and expected — that's the whole indie-dev ecosystem. Keep it fun, keep it buildable.