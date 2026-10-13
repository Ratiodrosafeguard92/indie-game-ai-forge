"""Entry point for the forge CLI. Typer app; thin over forge_core."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from forge_cli.bootstrap import load_env
from forge_core.pipeline import Pipeline
from forge_core.registry import build_default_pipeline
from forge_utils.logging import configure_logging

app = typer.Typer(help="AI full indie game generator — prompt in, project out.")
console = Console()


@app.command()
def generate(
    prompt: str = typer.Argument(..., help="Design prompt, or path to a .md/.txt brief."),
    out: Path = typer.Option(Path("forge_out/game"), "--out", "-o"),
    target: str = typer.Option("godot", "--target", "-t", help="godot|unity|igpack"),
    seed: Optional[int] = typer.Option(None, "--seed"),
    dry_run: bool = typer.Option(False, "--dry-run"),
) -> None:
    """Run the full pipeline and emit a playable project."""
    env = load_env()
    configure_logging(env.log_level)
    pipe = build_default_pipeline(env, target=target, seed=seed)
    report = pipe.run(prompt)
    if dry_run:
        console.print(report.summary())
        raise typer.Exit(0)
    console.print(report.summary())


@app.command()
def stages() -> None:
    """List pipeline stages in execution order."""
    for i, name in enumerate(Pipeline.default_stage_names()):
        console.print(f"{i:02d}  {name}")


if __name__ == "__main__":
    app()