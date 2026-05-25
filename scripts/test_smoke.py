#!/usr/bin/env python3
"""Smoke tests for obsidian-daily-curator-generic release package."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable


def run(args: list[str], cwd: Path | None = None) -> str:
    proc = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    if proc.returncode != 0:
        raise AssertionError(
            f"Command failed: {' '.join(args)}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
        )
    return proc.stdout


def assert_exists(path: Path) -> None:
    if not path.exists():
        raise AssertionError(f"Expected path to exist: {path}")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="odc-generic-smoke-") as td:
        vault = Path(td) / "Vault With Spaces"
        vault.mkdir()

        out = run([PY, str(ROOT / "scripts" / "bootstrap_vault.py"), "--vault", str(vault), "--dry-run"])
        if "No changes written" not in out:
            raise AssertionError("dry-run did not report no changes")
        if (vault / ".daily-curator").exists():
            raise AssertionError("dry-run created files")

        run([PY, str(ROOT / "scripts" / "bootstrap_vault.py"), "--vault", str(vault), "--apply"])
        assert_exists(vault / ".daily-curator" / "config.json")
        assert_exists(vault / "Templates" / "Quick Capture Template.md")

        config = json.loads((vault / ".daily-curator" / "config.json").read_text(encoding="utf-8"))
        assert config["paths"]["daily_notes"] == "Daily"

        out = run([PY, str(ROOT / "scripts" / "prepare_quick_capture.py"), "--vault", str(vault), "--date", "2026-01-02"])
        if "created: Daily/2026-01-02.md" not in out:
            raise AssertionError(f"unexpected prepare output: {out}")
        assert_exists(vault / "Daily" / "2026-01-02.md")

        before = (vault / "Daily" / "2026-01-02.md").read_text(encoding="utf-8")
        out = run([PY, str(ROOT / "scripts" / "prepare_quick_capture.py"), "--vault", str(vault), "--date", "2026-01-02"])
        if "exists: Daily/2026-01-02.md" not in out:
            raise AssertionError("prepare should skip existing note")
        after = (vault / "Daily" / "2026-01-02.md").read_text(encoding="utf-8")
        if before != after:
            raise AssertionError("existing quick capture was overwritten")

        out = run([PY, str(ROOT / "scripts" / "scan_vault.py"), "--vault", str(vault), "--date", "2026-01-02"])
        if "Daily/2026-01-02.md" not in out or "Config: found" not in out:
            raise AssertionError(f"scan did not find expected files:\n{out}")

    print("Smoke tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
