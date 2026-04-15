from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .engine import DestinationConflictError, ValidationError, build_scaffold_plan


class Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.exit(3, f"usage error: {message}\n")


def build_parser() -> argparse.ArgumentParser:
    parser = Parser(prog="new-scaffold", description="Generate a project scaffold.")
    parser.add_argument("name", help="Project name in kebab-case.")
    parser.add_argument("--base-path", required=True, help="Destination base path.")
    parser.add_argument(
        "--type",
        choices=("generic", "api", "bot", "worker"),
        default="generic",
        help="Project scaffold type.",
    )
    parser.add_argument("--owner", default="", help="Expected owner label.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow creating inside an existing empty destination directory.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show planned actions only.")
    parser.add_argument(
        "--output",
        choices=("json", "text"),
        default="text",
        help="Output format.",
    )
    parser.add_argument(
        "--with-gitignore",
        action="store_true",
        help="Create a base .gitignore file.",
    )
    parser.add_argument(
        "--with-makefile",
        action="store_true",
        help="Create a base Makefile.",
    )
    parser.add_argument(
        "--with-scripts",
        action="store_true",
        help="Create base operational scripts.",
    )
    return parser


def render_text(result: dict) -> str:
    lines = [
        f"project: {result['project']}",
        f"type: {result['type']}",
        f"destination: {result['destination']}",
        f"dry_run: {str(result['dry_run']).lower()}",
        f"status: {result['status']}",
    ]
    if result["summary"]:
        for key in ("create_dir", "create_file", "skip", "unchanged"):
            if result["summary"].get(key, 0):
                lines.append(f"{key}: {result['summary'][key]}")
    if result["actions"]:
        lines.append("actions:")
        for action in result["actions"]:
            lines.append(f"  - {action['kind']}: {action['path']}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = build_scaffold_plan(
            name=args.name,
            base_path=Path(args.base_path),
            scaffold_type=args.type,
            owner=args.owner,
            force=args.force,
            dry_run=args.dry_run,
            output=args.output,
            with_gitignore=args.with_gitignore,
            with_makefile=args.with_makefile,
            with_scripts=args.with_scripts,
        )
    except ValidationError as exc:
        sys.stderr.write(f"validation error: {exc}\n")
        return 2
    except DestinationConflictError as exc:
        sys.stderr.write(f"destination conflict: {exc}\n")
        return 4

    if args.output == "json":
        sys.stdout.write(json.dumps(result, indent=2, sort_keys=True))
        sys.stdout.write("\n")
    else:
        sys.stdout.write(render_text(result))
        sys.stdout.write("\n")
    return 0
