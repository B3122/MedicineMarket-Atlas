from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

from conftest import make_project, valid_json_artifact, write_artifact


REPO_ROOT = Path(__file__).resolve().parents[1]
PI_DIR = REPO_ROOT / ".pi"
if str(PI_DIR) not in sys.path:
    sys.path.insert(0, str(PI_DIR))

from scripts.checkpoint import (  # noqa: E402
    build_progress,
    hash_file,
    load_chain,
    restart_project,
    sanitize_output_path,
    validate_artifact,
    write_progress,
)


def _load_check_progress_module():
    module_path = REPO_ROOT / ".pi" / "scripts" / "check-progress.py"
    spec = importlib.util.spec_from_file_location("check_progress", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


check_progress = _load_check_progress_module()


def _run_full_market_check(project_dir: Path, capsys: pytest.CaptureFixture[str]) -> dict:
    exit_code = check_progress.main(
        [str(project_dir), "--chain", "full-market-review", "--json"]
    )
    captured = capsys.readouterr()
    assert exit_code == 0, captured.err
    return json.loads(captured.out)


def _statuses(progress: dict) -> dict[str, str]:
    return {step["id"]: step["status"] for step in progress["steps"]}


def test_validate_artifact_accepts_valid_json(tmp_path: Path) -> None:
    artifact = tmp_path / "valid.json"
    artifact.write_text(
        json.dumps(
            {
                "summary": "valid artifact with enough content for checkpoint validation",
                "items": ["alpha", "beta"],
            }
        ),
        encoding="utf-8",
    )

    assert validate_artifact(artifact) == (True, None)


def test_validate_artifact_rejects_markdown_without_heading(tmp_path: Path) -> None:
    artifact = tmp_path / "invalid.md"
    artifact.write_text(
        "This markdown artifact has enough plain text to exceed fifty bytes but lacks a heading.",
        encoding="utf-8",
    )

    assert validate_artifact(artifact) == (False, "missing markdown heading")


def test_validate_artifact_rejects_error_prefix(tmp_path: Path) -> None:
    artifact = tmp_path / "error.json"
    artifact.write_text(
        "ERROR: this agent could not produce the expected artifact, despite enough bytes.",
        encoding="utf-8",
    )

    assert validate_artifact(artifact) == (False, "error-prefixed")


def test_sanitize_output_path_accepts_chain_outputs_child(tmp_path: Path) -> None:
    project_dir = tmp_path / "project"
    expected = (project_dir / "chain-outputs" / "01-plan.json").resolve()

    assert sanitize_output_path(project_dir, "01-plan.json") == expected


def test_sanitize_output_path_rejects_path_traversal(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="may not contain"):
        sanitize_output_path(tmp_path / "project", "../etc/passwd")


def test_sanitize_output_path_rejects_absolute_path(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="absolute"):
        sanitize_output_path(tmp_path / "project", str(tmp_path / "outside.json"))


def test_load_chain_json_flattens_parallel_steps() -> None:
    chain = load_chain(REPO_ROOT / ".pi/chains/full-market-review.chain.json")

    assert chain["name"] == "full-market-review"
    assert [step["id"] for step in chain["steps"]] == [
        "plan",
        "market",
        "academic",
        "regulatory",
        "normalized",
        "competitors",
        "claims",
        "report",
        "audit",
    ]
    assert chain["steps"][4]["reads"] == ["02-market.json", "04-regulatory.json"]


def test_load_chain_json_suffixes_duplicate_ids(tmp_path: Path) -> None:
    chain_path = tmp_path / "duplicate.chain.json"
    chain_path.write_text(
        json.dumps(
            {
                "name": "duplicate-test",
                "chain": [
                    {
                        "agent": "task-planner",
                        "as": "plan",
                        "phase": "Planning",
                        "label": "Plan",
                        "output": "01-plan.json",
                    },
                    {
                        "agent": "task-planner",
                        "as": "plan",
                        "phase": "Planning",
                        "label": "Plan again",
                        "output": "02-plan.json",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    chain = load_chain(chain_path)

    assert [step["id"] for step in chain["steps"]] == ["plan", "plan-1"]


def test_load_chain_markdown_splits_plus_joined_reads() -> None:
    chain = load_chain(REPO_ROOT / ".pi/chains/quick-competitor-review.chain.md")

    normalized = chain["steps"][2]

    assert chain["name"] == "quick-competitor-review"
    assert normalized["id"] == "normalized"
    assert normalized["reads"] == ["01-quick-review-plan.md", "02-quick-market-findings.md"]


def test_fresh_project_all_pending(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    project_dir = make_project(tmp_path)

    progress = _run_full_market_check(project_dir, capsys)

    assert all(status == "pending" for status in _statuses(progress).values())
    assert not (project_dir / "progress.json").exists()
    assert REPO_ROOT / "projects" not in project_dir.parents


def test_completed_first_step(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    project_dir = make_project(tmp_path)
    write_artifact(project_dir, "01-plan.json", valid_json_artifact("plan"))

    progress = _run_full_market_check(project_dir, capsys)
    statuses = _statuses(progress)

    assert statuses["plan"] == "completed"
    assert all(
        status == "pending" for step_id, status in statuses.items() if step_id != "plan"
    )


def test_partial_parallel_research(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    project_dir = make_project(tmp_path)
    write_artifact(project_dir, "01-plan.json", valid_json_artifact("plan"))
    write_artifact(project_dir, "02-market.json", valid_json_artifact("market"))

    progress = _run_full_market_check(project_dir, capsys)
    statuses = _statuses(progress)

    assert statuses["plan"] == "completed"
    assert statuses["market"] == "completed"
    assert statuses["academic"] == "pending"
    assert statuses["regulatory"] == "pending"
    assert statuses["normalized"] == "pending"


def test_dependency_invalidation(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    project_dir = make_project(tmp_path)
    write_artifact(project_dir, "01-plan.json", valid_json_artifact("plan"))
    write_artifact(project_dir, "04-regulatory.json", valid_json_artifact("regulatory"))
    write_artifact(project_dir, "05-normalized-products.json", valid_json_artifact("normalized"))

    progress = _run_full_market_check(project_dir, capsys)
    statuses = _statuses(progress)

    normalized_step = next(step for step in progress["steps"] if step["id"] == "normalized")

    assert statuses["market"] == "pending"
    assert statuses["regulatory"] == "completed"
    assert statuses["normalized"] == "pending"
    assert "output_valid" not in normalized_step


def test_restart_creates_backup(tmp_path: Path) -> None:
    project_dir = make_project(tmp_path)
    chain_path = REPO_ROOT / ".pi" / "chains" / "full-market-review.chain.json"
    config_path = project_dir / "config.json"
    brief_path = project_dir / "brief.md"
    chain = load_chain(chain_path)
    write_artifact(project_dir, "01-plan.json", valid_json_artifact("plan"))
    progress = build_progress(
        chain,
        project_dir,
        hash_file(chain_path),
        hash_file(config_path),
        hash_file(brief_path),
    )
    write_progress(progress, project_dir, chain["name"])

    backup_dir = restart_project(project_dir, chain, chain_path, config_path, brief_path)

    assert backup_dir.exists()
    assert (backup_dir / "chain-outputs" / "01-plan.json").exists()
    assert (backup_dir / "progress.json").exists()
    assert list((project_dir / "chain-outputs").iterdir()) == []

    fresh_progress = json.loads((project_dir / "progress.json").read_text(encoding="utf-8"))
    assert all(status == "pending" for status in _statuses(fresh_progress).values())
