from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import jsonschema


ERROR_PREFIXES = ("I do not have", "ERROR:")
METADATA_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$")


def load_chain(chain_path: Path) -> dict:
    r"""Parse .chain.json or .chain.md and return a normalized dict:
    {
      "name": str,
      "steps": [
        {"id": str, "phase": str, "label": str, "output": str, "reads": list[str]}
      ]
    }
    For JSON chains, read the top-level "chain" array. For each step dict:
      - id = value of "as" (required) or agent name with suffix if duplicated.
      - output = value of "output".
      - reads = value of "reads" (list), normalized to a list of strings.
      - phase = value of "phase".
      - label = value of "label".
    For parallel groups in JSON chains, do NOT create a progress step for the group;
    create one step per child in the "parallel" array.
    For Markdown chains, the file has YAML frontmatter (`---` ... `---`) followed by
    one or more `## agent-name` sections. Parse frontmatter for `name`. For each
    `## agent-name` section, read contiguous metadata lines immediately under the
    heading. A metadata line must match `^key:\s*(.*)$`; stop at the first blank
    line or non-metadata line. A `reads` value may be a `+`-joined string
    (e.g. `01-plan.md+02-market.md`); split on `+` into a list.
    """
    chain_path = Path(chain_path)
    if chain_path.suffix == ".json":
        return _load_json_chain(chain_path)
    if chain_path.suffix == ".md":
        return _load_markdown_chain(chain_path)
    raise ValueError(f"unsupported chain file type: {chain_path.suffix}")


def list_artifacts(project_dir: Path) -> list[Path]:
    """Return valid artifact files in <project_dir>/chain-outputs/."""
    chain_outputs = Path(project_dir) / "chain-outputs"
    if not chain_outputs.exists():
        return []
    return sorted(
        path for path in chain_outputs.iterdir() if path.is_file() and validate_artifact(path)[0]
    )


def validate_artifact(path: Path) -> tuple[bool, str | None]:
    """Return (valid, reason). For .json: parseable JSON, >50 bytes, not error-prefixed.
    For .md: contains a markdown heading, >50 bytes, not error-prefixed.
    For other files: >50 bytes, not error-prefixed.
    """
    path = Path(path)
    if not path.exists():
        return False, "missing file"
    if not path.is_file():
        return False, "not a file"
    if path.stat().st_size <= 50:
        return False, "file too small"

    text = path.read_text(encoding="utf-8", errors="replace")
    stripped = text.lstrip()
    if any(stripped.startswith(prefix) for prefix in ERROR_PREFIXES):
        return False, "error-prefixed"

    if path.suffix == ".json":
        try:
            json.loads(text)
        except json.JSONDecodeError:
            return False, "invalid json"
    elif path.suffix == ".md" and not _contains_markdown_heading(text):
        return False, "missing markdown heading"
    return True, None


def sanitize_output_path(project_dir: Path, filename: str) -> Path:
    """Reject absolute paths, paths with .., and paths resolving outside
    <project_dir>/chain-outputs/. Return the resolved Path inside chain-outputs/.
    """
    if not filename:
        raise ValueError("output filename is empty")

    relative = Path(filename)
    if relative.is_absolute():
        raise ValueError("absolute output paths are not allowed")
    if ".." in relative.parts:
        raise ValueError("output paths may not contain '..'")

    chain_outputs = (Path(project_dir) / "chain-outputs").resolve()
    candidate = (chain_outputs / relative).resolve()
    try:
        candidate.relative_to(chain_outputs)
    except ValueError as exc:
        raise ValueError("output path resolves outside chain-outputs") from exc
    if candidate == chain_outputs:
        raise ValueError("output filename must name a file")
    return candidate


def build_progress(
    chain: dict,
    project_dir: Path,
    chain_hash: str,
    config_hash: str,
    brief_hash: str,
) -> dict:
    """Create initial progress.json matching progress.schema.json."""
    progress = {
        "chain_name": str(chain["name"]),
        "chain_hash": chain_hash,
        "config_hash": config_hash,
        "brief_hash": brief_hash,
        "last_run": _now_iso(),
        "steps": [
            {
                "id": str(step["id"]),
                "phase": str(step["phase"]),
                "label": str(step["label"]),
                "status": "pending",
                "output": str(step["output"]),
            }
            for step in chain.get("steps", [])
        ],
    }
    _validate_progress(progress)
    return progress


def hash_file(path: Path) -> str:
    """SHA-256 hex digest of file content."""
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def detect_input_changes(
    progress: dict,
    chain_path: Path,
    config_path: Path,
    brief_path: Path,
) -> list[str]:
    """Compare stored hashes with current files; return list of warnings
    (empty if none).
    """
    checks = (
        ("chain_hash", chain_path, "Chain file has changed"),
        ("config_hash", config_path, "Project configuration has changed"),
        ("brief_hash", brief_path, "Project brief has changed"),
    )
    warnings: list[str] = []
    for key, path, message in checks:
        try:
            current_hash = hash_file(path)
        except FileNotFoundError:
            warnings.append(f"{message}: {path} is missing")
            continue
        if progress.get(key) != current_hash:
            warnings.append(
                f"{message}: stored {progress.get(key, 'unknown')}, current {current_hash}"
            )
    return warnings


def update_progress_from_artifacts(progress: dict, chain: dict, project_dir: Path) -> dict:
    """Mark step completed only if output file exists+valid AND all reads files
    exist+valid. Otherwise pending. Keep failed status if output/read still invalid.
    """
    current_steps = {step.get("id"): step for step in progress.get("steps", [])}
    checked_steps = []
    completed_at = _now_iso()

    for chain_step in chain.get("steps", []):
        existing_step = current_steps.get(chain_step["id"], {})
        output_valid, output_reason = _validate_named_artifact(
            project_dir, str(chain_step["output"])
        )
        read_results = [
            _validate_named_artifact(project_dir, read_name)
            for read_name in _normalize_reads(chain_step.get("reads"))
        ]
        reads_valid = all(valid for valid, _reason in read_results)

        step = {
            "id": str(chain_step["id"]),
            "phase": str(chain_step["phase"]),
            "label": str(chain_step["label"]),
            "status": "pending",
            "output": str(chain_step["output"]),
        }

        if output_valid and reads_valid:
            step["status"] = "completed"
            step["output_valid"] = True
            step["completed_at"] = existing_step.get("completed_at", completed_at)
        elif existing_step.get("status") == "failed":
            step["status"] = "failed"
            step["output_valid"] = False
            step["completed_at"] = existing_step.get("completed_at", completed_at)
            step["error"] = existing_step.get(
                "error", _artifact_error_message(output_reason, read_results)
            )
        checked_steps.append(step)

    updated = {
        "chain_name": progress["chain_name"],
        "chain_hash": progress["chain_hash"],
        "config_hash": progress["config_hash"],
        "brief_hash": progress["brief_hash"],
        "last_run": _now_iso(),
        "steps": checked_steps,
    }
    _validate_progress(updated)
    return updated


def write_progress(progress: dict, project_dir: Path, chain_name: str) -> None:
    """Atomic write: write to <project_dir>/progress.json.tmp, then os.replace
    to progress.json.
    """
    project_dir = Path(project_dir)
    project_dir.mkdir(parents=True, exist_ok=True)

    progress_to_write = dict(progress)
    progress_to_write["chain_name"] = chain_name
    progress_to_write["last_run"] = _now_iso()
    _validate_progress(progress_to_write)

    tmp_path = project_dir / "progress.json.tmp"
    final_path = project_dir / "progress.json"
    with tmp_path.open("w", encoding="utf-8") as handle:
        json.dump(progress_to_write, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    os.replace(tmp_path, final_path)


def restart_project(
    project_dir: Path,
    chain: dict,
    chain_path: Path,
    config_path: Path,
    brief_path: Path,
) -> Path:
    """Backup chain-outputs/ and progress.json to
    chain-outputs-backup-YYYYMMDD-HHmmss/. Then delete the original chain-outputs/
    directory and progress.json. Then recreate an empty chain-outputs/ directory
    and write a fresh pending progress.json. Return backup directory path.
    Use shutil.copytree / shutil.copy2 / shutil.rmtree; no shell commands.
    """
    project_dir = Path(project_dir)
    chain_outputs = project_dir / "chain-outputs"
    progress_path = project_dir / "progress.json"
    backup_dir = _new_backup_dir(project_dir)
    backup_dir.mkdir(parents=True, exist_ok=False)

    if chain_outputs.exists():
        shutil.copytree(chain_outputs, backup_dir / "chain-outputs")
    if progress_path.exists():
        shutil.copy2(progress_path, backup_dir / "progress.json")

    if chain_outputs.exists():
        shutil.rmtree(chain_outputs)
    if progress_path.exists():
        progress_path.unlink()
    chain_outputs.mkdir(parents=True, exist_ok=True)

    fresh_progress = build_progress(
        chain,
        project_dir,
        hash_file(chain_path),
        hash_file(config_path),
        hash_file(brief_path),
    )
    write_progress(fresh_progress, project_dir, str(chain["name"]))
    return backup_dir


def _load_json_chain(chain_path: Path) -> dict:
    data = json.loads(chain_path.read_text(encoding="utf-8"))
    steps: list[dict[str, Any]] = []
    used_ids: dict[str, int] = {}
    for item in data.get("chain", []):
        children = item.get("parallel") if isinstance(item, dict) else None
        if children is not None:
            for child in children:
                steps.append(_normalize_chain_step(child, used_ids))
        else:
            steps.append(_normalize_chain_step(item, used_ids))
    return {"name": str(data["name"]), "steps": steps}


def _load_markdown_chain(chain_path: Path) -> dict:
    lines = chain_path.read_text(encoding="utf-8").splitlines()
    frontmatter, body_start = _parse_frontmatter(lines)
    used_ids: dict[str, int] = {}
    steps: list[dict[str, Any]] = []

    line_index = body_start
    while line_index < len(lines):
        line = lines[line_index]
        if line.startswith("## "):
            agent_name = line[3:].strip()
            metadata = _parse_metadata_lines(lines, line_index + 1)
            base_id = metadata.get("as") or agent_name
            steps.append(
                {
                    "id": _deduplicate_id(base_id, used_ids),
                    "phase": metadata.get("phase", ""),
                    "label": metadata.get("label", agent_name),
                    "output": metadata.get("output", "not_applicable"),
                    "reads": _normalize_reads(metadata.get("reads")),
                }
            )
        line_index += 1
    return {"name": frontmatter.get("name", chain_path.stem), "steps": steps}


def _parse_frontmatter(lines: list[str]) -> tuple[dict[str, str], int]:
    if not lines or lines[0].strip() != "---":
        return {}, 0

    metadata: dict[str, str] = {}
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return metadata, index + 1
        match = METADATA_RE.match(line)
        if match:
            metadata[match.group(1)] = match.group(2).strip()
    raise ValueError("unterminated markdown frontmatter")


def _parse_metadata_lines(lines: list[str], start_index: int) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in lines[start_index:]:
        if not line.strip():
            break
        match = METADATA_RE.match(line)
        if not match:
            break
        metadata[match.group(1)] = match.group(2).strip()
    return metadata


def _normalize_chain_step(step: dict, used_ids: dict[str, int]) -> dict:
    if not isinstance(step, dict):
        raise ValueError("chain step must be an object")
    base_id = step.get("as") or step.get("agent")
    if not base_id:
        raise ValueError("chain step requires 'as' or 'agent'")
    return {
        "id": _deduplicate_id(str(base_id), used_ids),
        "phase": str(step.get("phase", "")),
        "label": str(step.get("label", step.get("agent", base_id))),
        "output": str(step.get("output", "not_applicable")),
        "reads": _normalize_reads(step.get("reads")),
    }


def _deduplicate_id(base_id: str, used_ids: dict[str, int]) -> str:
    count = used_ids.get(base_id, 0)
    used_ids[base_id] = count + 1
    if count == 0:
        return base_id
    return f"{base_id}-{count}"


def _normalize_reads(value: Any) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, str):
        return [part.strip() for part in value.split("+") if part.strip()]
    if isinstance(value, list):
        reads: list[str] = []
        for item in value:
            if isinstance(item, str):
                reads.extend(_normalize_reads(item))
            else:
                reads.append(str(item))
        return reads
    return [str(value)]


def _validate_named_artifact(project_dir: Path, filename: str) -> tuple[bool, str | None]:
    try:
        path = sanitize_output_path(project_dir, filename)
    except ValueError as exc:
        return False, str(exc)
    return validate_artifact(path)


def _artifact_error_message(
    output_reason: str | None, read_results: list[tuple[bool, str | None]]
) -> str:
    if output_reason:
        return f"output invalid: {output_reason}"
    for valid, reason in read_results:
        if not valid and reason:
            return f"read invalid: {reason}"
    return "unknown"


def _contains_markdown_heading(text: str) -> bool:
    return any(line.startswith("#") for line in text.splitlines())


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _validate_progress(progress: dict) -> None:
    schema_path = Path(__file__).resolve().parent.parent / "schemas" / "progress.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    jsonschema.validate(progress, schema)


def _new_backup_dir(project_dir: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = project_dir / f"chain-outputs-backup-{timestamp}"
    suffix = 1
    while backup_dir.exists():
        backup_dir = project_dir / f"chain-outputs-backup-{timestamp}-{suffix}"
        suffix += 1
    return backup_dir
