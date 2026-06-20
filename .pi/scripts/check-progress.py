from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


pi_dir = Path(__file__).resolve().parent.parent
repo_root = pi_dir.parent
if str(pi_dir) not in sys.path:
    sys.path.insert(0, str(pi_dir))

from scripts.checkpoint import (  # noqa: E402
    build_progress,
    detect_input_changes,
    hash_file,
    load_chain,
    restart_project,
    update_progress_from_artifacts,
)


SUCCESS = 0
INVALID_ARGS = 1
CHAIN_NOT_FOUND = 2
INTERNAL_ERROR = 3


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        project_dir = Path(args.project_dir).expanduser().resolve()
        if not project_dir.is_dir():
            print(f"error: project directory not found: {project_dir}", file=sys.stderr)
            return INVALID_ARGS

        chain_path = _resolve_chain_path(args.chain)
        if chain_path is None:
            print(f"error: chain file not found for: {args.chain}", file=sys.stderr)
            return CHAIN_NOT_FOUND

        config_path = project_dir / "config.json"
        brief_path = project_dir / "brief.md"
        missing_inputs = [str(path) for path in (config_path, brief_path) if not path.is_file()]
        if missing_inputs:
            print(f"error: missing project input(s): {', '.join(missing_inputs)}", file=sys.stderr)
            return INVALID_ARGS

        chain = load_chain(chain_path)

        if args.restart:
            if not args.yes and not _confirm_restart(project_dir):
                print("restart cancelled", file=sys.stderr)
                return SUCCESS
            backup_dir = restart_project(project_dir, chain, chain_path, config_path, brief_path)
            print(f"Restarted project; backup: {backup_dir}", file=sys.stderr)
            progress = _load_progress(project_dir, chain, chain_path, config_path, brief_path)
        else:
            progress = _load_progress(project_dir, chain, chain_path, config_path, brief_path)
            for warning in detect_input_changes(progress, chain_path, config_path, brief_path):
                print(f"WARNING: {warning}", file=sys.stderr)
            progress = update_progress_from_artifacts(progress, chain, project_dir)

        if args.json:
            print(json.dumps(progress, ensure_ascii=False, indent=2))
        else:
            _print_table(progress)
        return SUCCESS
    except Exception as exc:
        print(f"internal error: {exc}", file=sys.stderr)
        return INTERNAL_ERROR


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect or restart checkpoint progress for a research project."
    )
    parser.add_argument("project_dir", help="Project directory containing config.json and brief.md")
    parser.add_argument("--chain", required=True, help="Chain name, e.g. full-market-review")
    parser.add_argument("--restart", action="store_true", help="Backup and clear old artifacts")
    parser.add_argument("--yes", action="store_true", help="Skip restart confirmation prompt")
    parser.add_argument("--json", action="store_true", help="Print progress as JSON")
    return parser


def _resolve_chain_path(chain_name: str) -> Path | None:
    json_path = pi_dir / "chains" / f"{chain_name}.chain.json"
    if json_path.is_file():
        return json_path
    markdown_path = pi_dir / "chains" / f"{chain_name}.chain.md"
    if markdown_path.is_file():
        return markdown_path
    return None


def _load_progress(
    project_dir: Path,
    chain: dict[str, Any],
    chain_path: Path,
    config_path: Path,
    brief_path: Path,
) -> dict[str, Any]:
    progress_path = project_dir / "progress.json"
    if progress_path.is_file():
        try:
            progress = json.loads(progress_path.read_text(encoding="utf-8"))
            _validate_progress_shape(progress)
            if progress.get("chain_name") == chain["name"]:
                return progress
            print(
                "WARNING: progress.json is for "
                f"'{progress.get('chain_name')}', not '{chain['name']}'; using fresh progress",
                file=sys.stderr,
            )
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            print(f"WARNING: progress.json is invalid; using fresh progress ({exc})", file=sys.stderr)

    return build_progress(
        chain,
        project_dir,
        hash_file(chain_path),
        hash_file(config_path),
        hash_file(brief_path),
    )


def _validate_progress_shape(progress: Any) -> None:
    if not isinstance(progress, dict):
        raise ValueError("progress root is not an object")
    required = {"chain_name", "chain_hash", "config_hash", "brief_hash", "last_run", "steps"}
    missing = sorted(required - set(progress))
    if missing:
        raise ValueError(f"missing required progress field(s): {', '.join(missing)}")
    if not isinstance(progress["steps"], list):
        raise ValueError("progress steps is not a list")


def _confirm_restart(project_dir: Path) -> bool:
    response = input(f"Restart project '{project_dir}' and backup existing artifacts? [y/N] ")
    return response.strip().lower() in {"y", "yes"}


def _print_table(progress: dict[str, Any]) -> None:
    rows = [
        (
            str(step.get("id", "")),
            str(step.get("phase", "")),
            str(step.get("label", "")),
            str(step.get("status", "")),
        )
        for step in progress.get("steps", [])
    ]
    headers = ("Step", "Phase", "Label", "Status")
    widths = [len(header) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))

    print(f"Project progress: {progress.get('chain_name', 'unknown')}")
    print(_format_row(headers, widths))
    print(_format_row(tuple("-" * width for width in widths), widths))
    for row in rows:
        print(_format_row(row, widths))


def _format_row(row: tuple[str, str, str, str], widths: list[int]) -> str:
    return " | ".join(value.ljust(widths[index]) for index, value in enumerate(row))


if __name__ == "__main__":
    raise SystemExit(main())
