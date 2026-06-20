from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PI_DIR = REPO_ROOT / ".pi"

if str(PI_DIR) not in sys.path:
    sys.path.insert(0, str(PI_DIR))


def make_project(
    tmp_path: Path,
    brief: str = "# Test brief\n\nResearch a temporary checkpoint fixture project only.",
    config: dict[str, Any] | None = None,
) -> Path:
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    (project_dir / "chain-outputs").mkdir()
    (project_dir / "brief.md").write_text(brief, encoding="utf-8")
    (project_dir / "config.json").write_text(
        json.dumps(config or {"market": "test", "jurisdiction": "test"}, indent=2),
        encoding="utf-8",
    )
    return project_dir


def write_artifact(project_dir: Path, filename: str, content: Any) -> Path:
    artifact_path = project_dir / "chain-outputs" / filename
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, str):
        text = content
    else:
        text = json.dumps(content, ensure_ascii=False, indent=2)
    artifact_path.write_text(text, encoding="utf-8")
    return artifact_path


def valid_json_artifact(label: str) -> dict[str, Any]:
    return {
        "label": label,
        "summary": "valid checkpoint fixture artifact with enough content for validation",
        "items": ["alpha", "beta", "gamma"],
    }
