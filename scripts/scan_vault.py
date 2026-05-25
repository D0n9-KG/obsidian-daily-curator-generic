#!/usr/bin/env python3
"""Read-only vault scan for obsidian-daily-curator-generic."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from copy import deepcopy
from datetime import datetime, date
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = SKILL_ROOT / "references" / "default-config.json"


def load_default_config() -> dict:
    return json.loads(DEFAULT_CONFIG_PATH.read_text(encoding="utf-8"))


def deep_merge(base: dict, override: dict) -> dict:
    out = deepcopy(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config(vault: Path, config_rel: str | None) -> tuple[dict, Path, bool]:
    default = load_default_config()
    rel = config_rel or default["paths"]["config"]
    path = vault / rel
    if path.exists():
        return deep_merge(default, json.loads(path.read_text(encoding="utf-8"))), path, True
    return default, path, False


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Scan vault for daily curation context.")
    p.add_argument("--vault", default=".")
    p.add_argument("--date", default=None, help="Target date YYYY-MM-DD; default today")
    p.add_argument("--config", default=None, help="Config path relative to vault")
    p.add_argument("--limit", type=int, default=30)
    return p.parse_args()


def rel(path: Path, vault: Path) -> str:
    return path.relative_to(vault).as_posix()


def sha12(path: Path) -> str:
    h = hashlib.sha256()
    try:
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()[:12]
    except OSError:
        return "unreadable"


def should_skip_dir(path: Path, vault: Path, excludes: set[str]) -> bool:
    r = rel(path, vault) if path != vault else ""
    name = path.name
    return name in excludes or r in excludes or any(r.startswith(e.rstrip("/") + "/") for e in excludes)


def iter_markdown(vault: Path, config: dict):
    excludes = set(config.get("scan", {}).get("exclude_dirs", []))
    include_dirs = [vault / p for p in config.get("scan", {}).get("include_dirs", [])]
    roots = include_dirs if include_dirs else [vault]
    seen: set[Path] = set()
    for start in roots:
        if not start.exists():
            continue
        for root, dirs, files in os.walk(start):
            root_p = Path(root)
            dirs[:] = [d for d in dirs if not should_skip_dir(root_p / d, vault, excludes)]
            for name in files:
                if name.lower().endswith(".md"):
                    p = root_p / name
                    if p not in seen:
                        seen.add(p)
                        yield p


def date_patterns(target: date) -> list[str]:
    return [
        target.strftime("%Y-%m-%d"),
        target.strftime("%Y.%m.%d"),
        target.strftime("%Y_%m_%d"),
        f"{target.year}-{target.month}-{target.day}",
    ]


def score_daily_candidate(path: Path, vault: Path, target: date, config: dict) -> int:
    r = rel(path, vault).lower()
    name = path.stem.lower()
    patterns = [p.lower() for p in date_patterns(target)]
    score = 0
    if any(p in name for p in patterns):
        score += 60
    if any(p in r for p in patterns):
        score += 30
    daily_dir = config["paths"].get("daily_notes", "Daily").lower()
    if r.startswith(daily_dir.lower().rstrip("/") + "/"):
        score += 25
    if any(k in r for k in ["daily", "journal", "diary", "capture", "quick", "inbox"]):
        score += 15
    try:
        txt = path.read_text(encoding="utf-8", errors="ignore")[:2000].lower()
        if any(p in txt for p in patterns):
            score += 10
        if "type: quick-capture" in txt or "type: daily" in txt or "type: diary" in txt:
            score += 15
    except OSError:
        pass
    return score


def main() -> int:
    args = parse_args()
    vault = Path(args.vault).resolve()
    if not vault.exists():
        raise SystemExit(f"Vault path does not exist: {vault}")
    target = datetime.strptime(args.date, "%Y-%m-%d").date() if args.date else datetime.now().date()
    config, config_path, config_exists = load_config(vault, args.config)
    paths = config["paths"]

    md_files = list(iter_markdown(vault, config))
    candidates = []
    modified = []
    for p in md_files:
        st = p.stat()
        score = score_daily_candidate(p, vault, target, config)
        if score > 0:
            candidates.append((score, p, st.st_mtime, sha12(p)))
        if datetime.fromtimestamp(st.st_mtime).date() == target:
            modified.append((st.st_mtime, p, sha12(p)))

    candidates.sort(key=lambda x: (-x[0], -x[2], rel(x[1], vault)))
    modified.sort(key=lambda x: (-x[0], rel(x[1], vault)))

    print("# Daily curation scan")
    print(f"- Vault: `{vault}`")
    print(f"- Target date: `{target.isoformat()}`")
    print(f"- Config: {'found' if config_exists else 'missing'} `{rel(config_path, vault)}`")
    print(f"- Markdown files scanned: {len(md_files)}")

    print("\n## Managed files")
    managed_keys = ["rules", "architecture", "unresolved", "curation_log", "quick_capture_template", "daily_summary_template", "knowledge_card_template"]
    for k in managed_keys:
        p = vault / paths[k]
        print(f"- [{'x' if p.exists() else ' '}] `{paths[k]}`")

    print("\n## Configured folders")
    folder_keys = ["daily_notes", "daily_summaries", "knowledge_cards", "sources", "mocs", "projects", "templates"]
    for k in folder_keys:
        p = vault / paths[k]
        print(f"- [{'x' if p.exists() else ' '}] {k}: `{paths[k]}`")

    print("\n## Daily note candidates")
    if not candidates:
        print("- None found")
    else:
        for score, p, mtime, digest in candidates[:10]:
            ts = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
            print(f"- score={score} modified={ts} hash={digest} `{rel(p, vault)}`")

    print(f"\n## Markdown files modified on {target.isoformat()}")
    if not modified:
        print("- None found")
    else:
        for mtime, p, digest in modified[: args.limit]:
            ts = datetime.fromtimestamp(mtime).strftime("%H:%M")
            print(f"- {ts} hash={digest} `{rel(p, vault)}`")
        if len(modified) > args.limit:
            print(f"- ... {len(modified) - args.limit} more")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
