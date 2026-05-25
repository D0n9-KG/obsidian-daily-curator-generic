#!/usr/bin/env python3
"""Prepare a dated quick-capture note using generic daily-curator config."""
from __future__ import annotations

import argparse
import json
from copy import deepcopy
from datetime import datetime, timedelta
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


def load_config(vault: Path, config_rel: str | None) -> dict:
    default = load_default_config()
    rel = config_rel or default["paths"]["config"]
    path = vault / rel
    if path.exists():
        return deep_merge(default, json.loads(path.read_text(encoding="utf-8")))
    return default


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Prepare a dated quick-capture note.")
    p.add_argument("--vault", default=".")
    p.add_argument("--date", default=None, help="Date YYYY-MM-DD")
    p.add_argument("--tomorrow", action="store_true")
    p.add_argument("--config", default=None, help="Config path relative to vault")
    p.add_argument("--overwrite", action="store_true")
    return p.parse_args()


def rel(path: Path, vault: Path) -> str:
    return path.relative_to(vault).as_posix()


def render_template(template: str, ymd: str, title: str, source: str = "") -> str:
    dt = datetime.strptime(ymd, "%Y-%m-%d")
    replacements = {
        "{{date}}": ymd,
        "{{date:YYYY-MM-DD}}": ymd,
        "{{title}}": title,
        "{{source}}": source,
        "{{year}}": f"{dt.year:04d}",
        "{{month}}": f"{dt.month:02d}",
        "{{day}}": f"{dt.day:02d}",
    }
    out = template
    for k, v in replacements.items():
        out = out.replace(k, v)
    return out


def fallback_template(ymd: str) -> str:
    return f"""---
title: '{ymd} Quick Capture'
type: quick-capture
date: '{ymd}'
status: raw
tags:
  - type/quick-capture
---

# {ymd} Quick Capture

## Ideas

- [idea] 

## Knowledge

- [knowledge] 

## Code

- [code] 

## Resources

- [resource] 

## Questions

- [question] 

## Tasks

- [ ] 

## Raw paste area

"""


def main() -> int:
    args = parse_args()
    vault = Path(args.vault).resolve()
    if not vault.exists():
        raise SystemExit(f"Vault path does not exist: {vault}")

    config = load_config(vault, args.config)
    if args.date:
        ymd = args.date
        datetime.strptime(ymd, "%Y-%m-%d")
    elif args.tomorrow:
        ymd = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        ymd = datetime.now().strftime("%Y-%m-%d")

    paths = config["paths"]
    naming = config.get("naming", {})
    filename = naming.get("daily_note", "{date}.md").format(date=ymd)
    dest = vault / paths.get("daily_notes", "Daily") / filename
    template_path = vault / paths.get("quick_capture_template", "Templates/Quick Capture Template.md")
    title = f"{ymd} Quick Capture"

    if dest.exists() and not args.overwrite:
        print(f"exists: {rel(dest, vault)}")
        return 0

    if template_path.exists():
        content = render_template(template_path.read_text(encoding="utf-8"), ymd, title)
    else:
        content = fallback_template(ymd)

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8", newline="\n")
    print(f"created: {rel(dest, vault)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
