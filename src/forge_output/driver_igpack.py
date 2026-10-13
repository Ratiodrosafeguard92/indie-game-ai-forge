"""Alternative driver: pack the project into a single .igpack (zip) file."""
from __future__ import annotations

import json
import zipfile
from pathlib import Path

from forge_core.job import Job
from forge_models.game_project import GameProject
from forge_output.base import EmitReport


class IgpackDriver:
    name = "output.driver"
    requires = ("output.manifest",)

    def run(self, job: Job) -> Job:
        project: GameProject = job.ctx.scratch["project"]
        dest = job.ctx.scratch["env"].run_dir / f"{project.slug}.igpack"
        job.ctx.scratch["emit_report"] = self.emit(project, dest)
        return job

    def emit(self, project: GameProject, dest: Path) -> EmitReport:
        dest.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("manifest.json", json.dumps(project.to_manifest(), indent=2))
            for lvl in project.levels:
                z.writestr(f"levels/{lvl.id}.json", json.dumps(lvl.to_dict(), indent=2))
        return EmitReport(driver="igpack", files_written=1 + len(project.levels), dest=dest)