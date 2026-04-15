from __future__ import annotations

import unittest
import uuid
from contextlib import contextmanager
from pathlib import Path
import shutil

from lib.python.basic_scaffold.engine import (
    DestinationConflictError,
    ValidationError,
    build_scaffold_plan,
)


TEST_ROOT = Path(__file__).resolve().parents[1] / ".test-work"


@contextmanager
def workspace_tmpdir():
    path = TEST_ROOT / str(uuid.uuid4())
    path.mkdir(parents=True, exist_ok=False)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


class EngineTests(unittest.TestCase):
    def test_rejects_invalid_name(self) -> None:
        with workspace_tmpdir() as tmp:
            with self.assertRaises(ValidationError):
                build_scaffold_plan(
                    name="Bad_Name",
                    base_path=tmp,
                    scaffold_type="generic",
                    owner="alex",
                    force=False,
                    dry_run=True,
                    output="text",
                    with_gitignore=False,
                    with_makefile=False,
                    with_scripts=False,
                )

    def test_dry_run_for_bot_matches_expected_actions(self) -> None:
        with workspace_tmpdir() as tmp:
            result = build_scaffold_plan(
                name="soporte-bot",
                base_path=tmp,
                scaffold_type="bot",
                owner="alex",
                force=False,
                dry_run=True,
                output="json",
                with_gitignore=True,
                with_makefile=True,
                with_scripts=True,
            )
            self.assertEqual(result["status"], "planned")
            action_paths = {item["path"] for item in result["actions"]}
            self.assertIn(str(tmp / "soporte-bot" / "src" / "bot" / "main.py"), action_paths)
            self.assertIn(str(tmp / "soporte-bot" / "Makefile"), action_paths)
            self.assertIn(str(tmp / "soporte-bot" / ".gitignore"), action_paths)

    def test_existing_empty_destination_requires_force(self) -> None:
        with workspace_tmpdir() as tmp:
            destination = tmp / "demo-app"
            destination.mkdir()
            with self.assertRaises(DestinationConflictError):
                build_scaffold_plan(
                    name="demo-app",
                    base_path=tmp,
                    scaffold_type="generic",
                    owner="alex",
                    force=False,
                    dry_run=False,
                    output="text",
                    with_gitignore=False,
                    with_makefile=False,
                    with_scripts=False,
                )

    def test_second_run_is_idempotent(self) -> None:
        with workspace_tmpdir() as tmp:
            base_path = tmp
            first = build_scaffold_plan(
                name="demo-worker",
                base_path=base_path,
                scaffold_type="worker",
                owner="alex",
                force=False,
                dry_run=False,
                output="text",
                with_gitignore=False,
                with_makefile=False,
                with_scripts=False,
            )
            second = build_scaffold_plan(
                name="demo-worker",
                base_path=base_path,
                scaffold_type="worker",
                owner="alex",
                force=False,
                dry_run=False,
                output="text",
                with_gitignore=False,
                with_makefile=False,
                with_scripts=False,
            )
            self.assertEqual(first["status"], "created")
            self.assertEqual(second["status"], "no_changes")
            self.assertTrue(any(item["kind"] == "skip" for item in second["actions"]))

    def test_unmanaged_files_raise_conflict(self) -> None:
        with workspace_tmpdir() as tmp:
            base_path = tmp
            destination = base_path / "demo-api"
            destination.mkdir()
            (destination / "rogue.txt").write_text("unexpected", encoding="utf-8")
            with self.assertRaises(DestinationConflictError):
                build_scaffold_plan(
                    name="demo-api",
                    base_path=base_path,
                    scaffold_type="api",
                    owner="alex",
                    force=False,
                    dry_run=True,
                    output="text",
                    with_gitignore=False,
                    with_makefile=False,
                    with_scripts=False,
                )


if __name__ == "__main__":
    unittest.main()
