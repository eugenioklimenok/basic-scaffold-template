from __future__ import annotations

import json
import subprocess
import sys
import unittest
import uuid
from contextlib import contextmanager
from pathlib import Path
import shutil


REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_PATH = REPO_ROOT / "bin" / "new-scaffold"
TEST_ROOT = REPO_ROOT / ".test-work"


@contextmanager
def workspace_tmpdir():
    path = TEST_ROOT / str(uuid.uuid4())
    path.mkdir(parents=True, exist_ok=False)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


class SmokeCliTests(unittest.TestCase):
    def test_cli_dry_run_json(self) -> None:
        with workspace_tmpdir() as tmp:
            completed = subprocess.run(
                [
                    sys.executable,
                    str(CLI_PATH),
                    "demo-app",
                    "--base-path",
                    str(tmp),
                    "--type",
                    "generic",
                    "--dry-run",
                    "--output",
                    "json",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertEqual(payload["project"], "demo-app")
            self.assertEqual(payload["status"], "planned")

    def test_cli_returns_validation_exit_code(self) -> None:
        with workspace_tmpdir() as tmp:
            completed = subprocess.run(
                [
                    sys.executable,
                    str(CLI_PATH),
                    "DemoApp",
                    "--base-path",
                    str(tmp),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 2)
            self.assertIn("validation error", completed.stderr)


if __name__ == "__main__":
    unittest.main()
