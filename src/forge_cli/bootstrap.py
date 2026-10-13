"""Bootstrap: env loading, native bridge probe, run dir prep."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ForgeEnv:
    run_dir: Path
    plugin_dir: Path | None
    native_enabled: bool
    log_level: str


def load_env(run_root: Path | None = None) -> ForgeEnv:
    """Resolve forge runtime env from os.environ with sane defaults.

    Side effects: creates the run directory tree if missing.
    """
    root = run_root or Path(os.environ.get("FORGE_RUN_DIR", "forge_out")).resolve()
    root.mkdir(parents=True, exist_ok=True)
    (root / "runs").mkdir(exist_ok=True)

    plugin_dir = os.environ.get("FORGE_PLUGIN_DIR")
    return ForgeEnv(
        run_dir=root,
        plugin_dir=Path(plugin_dir).resolve() if plugin_dir else None,
        native_enabled=os.environ.get("FORGE_NATIVE", "0") == "1",
        log_level=os.environ.get("FORGE_LOG", "INFO").upper(),
    )