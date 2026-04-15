from __future__ import annotations

import os
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TEMPLATE_ROOT = Path(__file__).resolve().parents[3] / "templates" / "basic"


class ValidationError(Exception):
    pass


class DestinationConflictError(Exception):
    pass


@dataclass(frozen=True)
class Action:
    kind: str
    path: str

    def as_dict(self) -> dict[str, str]:
        return {"kind": self.kind, "path": self.path}


def _render_readme(name: str, scaffold_type: str, owner: str) -> str:
    owner_line = owner or "unassigned"
    return (
        f"# {name}\n\n"
        f"- Type: `{scaffold_type}`\n"
        f"- Expected owner: `{owner_line}`\n\n"
        "## Layout\n\n"
        "- `src/`\n"
        "- `config/`\n"
        "- `scripts/`\n"
        "- `docs/`\n"
        "- `tests/`\n"
        "- `logs/`\n"
        "- `tmp/`\n"
        "- `data/`\n"
    )


def _render_env(name: str, scaffold_type: str, owner: str) -> str:
    return (
        f"APP_NAME={name}\n"
        f"APP_TYPE={scaffold_type}\n"
        f"APP_OWNER={owner}\n"
        "APP_ENV=development\n"
    )


def _render_makefile() -> str:
    return (
        ".PHONY: help test lint fmt\n\n"
        "help:\n"
        "\t@echo \"Available targets: test lint fmt\"\n\n"
        "test:\n"
        "\t@echo \"TODO: define project test command\"\n\n"
        "lint:\n"
        "\t@echo \"TODO: define project lint command\"\n\n"
        "fmt:\n"
        "\t@echo \"TODO: define project format command\"\n"
    )


def _render_gitignore() -> str:
    return (
        "__pycache__/\n"
        "*.pyc\n"
        ".env\n"
        "logs/\n"
        "tmp/\n"
        ".pytest_cache/\n"
    )


def _render_script(name: str) -> str:
    return (
        "# Placeholder script\n"
        f"# Purpose: {name}\n"
        "# Replace this file with the command runner that fits your stack.\n"
    )


def _render_entrypoint(module_name: str) -> str:
    return (
        f"# {module_name} entrypoint placeholder\n\n"
        "# Define the real entrypoint for this project type.\n"
        "# Examples:\n"
        "# - API: app server bootstrap\n"
        "# - Bot: message polling or webhook handler\n"
        "# - Worker: queue consumer or scheduled job\n"
    )


def _load_template_files(name: str, scaffold_type: str, owner: str, with_gitignore: bool, with_makefile: bool, with_scripts: bool) -> dict[str, str]:
    files = {
        "README.md": _render_readme(name, scaffold_type, owner),
        ".env.example": _render_env(name, scaffold_type, owner),
    }
    if with_gitignore:
        files[".gitignore"] = _render_gitignore()
    if with_makefile:
        files["Makefile"] = _render_makefile()
    if with_scripts:
        files["scripts/bootstrap.example"] = _render_script("bootstrap")
        files["scripts/check.example"] = _render_script("check")
    if scaffold_type in {"api", "bot", "worker"}:
        module_dir = f"src/{scaffold_type}"
        files[f"{module_dir}/entrypoint.example"] = _render_entrypoint(scaffold_type)
    return files


def _expected_directories(scaffold_type: str, with_scripts: bool) -> list[str]:
    dirs = [
        "src",
        "config",
        "scripts",
        "docs",
        "tests",
        "logs",
        "tmp",
        "data",
    ]
    if scaffold_type in {"api", "bot", "worker"}:
        dirs.extend(["src", f"src/{scaffold_type}"])
    return sorted(set(dirs))


def _sorted_actions(actions: list[Action]) -> list[Action]:
    return sorted(actions, key=lambda item: (item.kind, item.path))


def _ensure_valid_name(name: str) -> None:
    if not NAME_PATTERN.match(name):
        raise ValidationError("name must use kebab-case")


def _ensure_base_path(base_path: Path) -> Path:
    try:
        resolved = base_path.expanduser().resolve()
    except OSError as exc:
        raise ValidationError(f"invalid base path: {base_path}") from exc
    if not resolved.exists():
        raise ValidationError("base path does not exist")
    if not resolved.is_dir():
        raise ValidationError("base path must be a directory")
    if not os.access(resolved, os.W_OK):
        raise ValidationError("base path is not writable")
    return resolved


def _scan_conflicts(destination: Path, expected_files: dict[str, str], expected_dirs: list[str]) -> tuple[list[Action], list[Action]]:
    planned: list[Action] = []
    unchanged: list[Action] = []

    for directory in expected_dirs:
        target_dir = destination / directory
        if target_dir.exists():
            unchanged.append(Action("unchanged", str(target_dir)))
        else:
            planned.append(Action("create_dir", str(target_dir)))

    for relative_path, content in sorted(expected_files.items()):
        target_file = destination / relative_path
        if target_file.exists():
            current = target_file.read_text(encoding="utf-8")
            if current != content:
                raise DestinationConflictError(f"file already exists with different content: {target_file}")
            unchanged.append(Action("skip", str(target_file)))
        else:
            planned.append(Action("create_file", str(target_file)))

    expected_paths = {str((destination / item).resolve()) for item in expected_dirs}
    expected_paths.update(str((destination / item).resolve()) for item in expected_files)
    for item in sorted(destination.rglob("*")):
        resolved = str(item.resolve())
        if resolved not in expected_paths:
            raise DestinationConflictError(f"destination contains unmanaged path: {item}")
    return _sorted_actions(planned), _sorted_actions(unchanged)


def build_scaffold_plan(
    *,
    name: str,
    base_path: Path,
    scaffold_type: str,
    owner: str,
    force: bool,
    dry_run: bool,
    output: str,
    with_gitignore: bool,
    with_makefile: bool,
    with_scripts: bool,
) -> dict:
    del output
    _ensure_valid_name(name)
    resolved_base = _ensure_base_path(base_path)
    destination = resolved_base / name
    expected_dirs = _expected_directories(scaffold_type, with_scripts)
    expected_files = _load_template_files(name, scaffold_type, owner, with_gitignore, with_makefile, with_scripts)

    planned: list[Action] = []
    unchanged: list[Action] = []

    if destination.exists():
        if not destination.is_dir():
            raise DestinationConflictError("destination exists and is not a directory")
        has_entries = any(destination.iterdir())
        if not has_entries:
            if not force:
                raise DestinationConflictError("destination exists and is empty; use --force to allow reuse")
        else:
            planned, unchanged = _scan_conflicts(destination, expected_files, expected_dirs)
    else:
        planned.append(Action("create_dir", str(destination)))
        for directory in expected_dirs:
            planned.append(Action("create_dir", str(destination / directory)))
        for relative_path in sorted(expected_files):
            planned.append(Action("create_file", str(destination / relative_path)))

    if destination.exists() and destination.is_dir() and not any(destination.iterdir()) and force:
        for directory in expected_dirs:
            planned.append(Action("create_dir", str(destination / directory)))
        for relative_path in sorted(expected_files):
            planned.append(Action("create_file", str(destination / relative_path)))

    planned = _sorted_actions(planned)
    unchanged = _sorted_actions(unchanged)

    if not dry_run:
        for action in planned:
            target = Path(action.path)
            if action.kind == "create_dir":
                target.mkdir(parents=True, exist_ok=True)
            elif action.kind == "create_file":
                target.parent.mkdir(parents=True, exist_ok=True)
                relative = target.relative_to(destination).as_posix()
                target.write_text(expected_files[relative], encoding="utf-8")

    summary = Counter(action.kind for action in planned + unchanged)
    status = "created" if planned else "no_changes"
    if dry_run and planned:
        status = "planned"

    return {
        "project": name,
        "type": scaffold_type,
        "destination": str(destination),
        "dry_run": dry_run,
        "status": status,
        "summary": dict(summary),
        "actions": [action.as_dict() for action in planned + unchanged],
    }
