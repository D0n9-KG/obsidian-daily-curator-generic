#!/usr/bin/env python3
"""Release checks for obsidian-daily-curator-generic."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable

FORBIDDEN_PATTERNS = [
    # Personal/local paths and accounts. Keep strings split so this checker
    # does not flag itself while scanning the release package.
    r"C:" + r"\\Users" + r"\\jd",
    r"C:/" + "Users/" + "jd",
    "D0n9" + "-KG",
    "Skill" + " Releases",
    r"\.codex" + r"\\skills",
    r"/\.codex/" + "skills",

    # Personal vault names / folders from the author's private setup.
    "Obsidian" + " Vault",
    "00 " + "工作台",
    "01 " + "Inbox",
    "02 " + "MOC",
    "03 " + "知识卡片",
    "04 " + "资料库",
    "05 " + "项目作品",
    "06 " + "求职面试",
    "07 " + "复盘输出",
    "LLM" + "学习",
    "研究生" + "算法求职",
    "知识" + "处理队列",
]
REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "LICENSE",
    "agents/openai.yaml",
    "references/default-config.json",
    "references/quality-checklist.md",
    "references/publishing-notes.md",
    "scripts/bootstrap_vault.py",
    "scripts/scan_vault.py",
    "scripts/prepare_quick_capture.py",
    "scripts/test_smoke.py",
    "scripts/check_release.py",
    "RELEASE_NOTES.md",
    "GITHUB_REPO_COPY.md",
    "examples/minimal-vault/Daily/2026-01-02.md",
    "examples/chinese-vault/Daily/2026-01-02.md",
]


def text_files():
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in {".git", "__pycache__"} for part in path.parts):
            continue
        if path.suffix.lower() in {".md", ".py", ".json", ".yaml", ".yml", ""}:
            yield path


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            errors.append(f"Missing required file: {rel}")

    for path in text_files():
        try:
            data = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"Non UTF-8 text file: {path.relative_to(ROOT)} ({exc})")
            continue
        for pat in FORBIDDEN_PATTERNS:
            if re.search(pat, data):
                errors.append(f"Forbidden pattern {pat!r} in {path.relative_to(ROOT)}")

    skill_path = ROOT / "SKILL.md"
    skill = skill_path.read_text(encoding="utf-8") if skill_path.exists() else ""
    if not skill.startswith("---\n") or "\n---\n" not in skill[4:]:
        errors.append("SKILL.md frontmatter is missing or malformed")
    if "name: obsidian-daily-curator-generic" not in skill:
        errors.append("SKILL.md name is wrong")
    if "description:" not in skill:
        errors.append("SKILL.md description is missing")

    smoke = subprocess.run([PY, str(ROOT / "scripts" / "test_smoke.py")], text=True, capture_output=True)
    if smoke.returncode != 0:
        errors.append("Smoke test failed:\n" + smoke.stdout + smoke.stderr)

    if errors:
        print("Release check failed:")
        for e in errors:
            print(f"- {e}")
        return 1

    print("Release check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
