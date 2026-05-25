#!/usr/bin/env python3
"""Bootstrap a vault for obsidian-daily-curator-generic.

Creates a configurable, layout-agnostic daily curation workspace. Safe by default:
- defaults to dry-run unless --apply is passed
- creates only missing files/folders
- never overwrites existing files unless --overwrite is passed
"""
from __future__ import annotations

import argparse
import json
from copy import deepcopy
from datetime import datetime
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


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Initialize a vault for generic daily curation.")
    p.add_argument("--vault", default=".", help="Vault root path")
    p.add_argument("--config", default=None, help="Config path relative to vault; default .daily-curator/config.json")
    p.add_argument("--apply", action="store_true", help="Create missing files/folders")
    p.add_argument("--dry-run", action="store_true", help="Preview actions without writing")
    p.add_argument("--overwrite", action="store_true", help="Overwrite managed files if they already exist")
    return p.parse_args()


def rel(path: Path, vault: Path) -> str:
    return path.relative_to(vault).as_posix()


def render_tokens(text: str, config: dict) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    replacements = {
        "{{date}}": today,
        "{{title}}": "",
        "{{source}}": "",
        "{date}": today,
    }
    out = text
    for k, v in replacements.items():
        out = out.replace(k, v)
    return out


def default_rules(config: dict) -> str:
    return """---
title: Daily Curator Rules
type: curation-rules
status: active
---

# Daily Curator Rules

Edit this file to teach the curator how your vault should be organized.

## Principles

- Preserve raw daily notes and imported sources.
- Distill reusable knowledge into atomic notes.
- Use source notes for saved articles, papers, videos, tools, and news.
- Use MOCs/maps as navigation pages, not dumping grounds.
- Put uncertain items in the unresolved queue.

## Item routing

| Item type | Default destination |
|---|---|
| idea | daily summary, project note, or reusable knowledge card |
| knowledge | knowledge cards |
| code | reusable knowledge card or project note |
| resource / paper / video | source notes; distill only understood claims |
| info | source note or summary; mark unverified if needed |
| task / question | summary and unresolved queue when follow-up is needed |
| reflection | daily summary |

## Naming

- Daily note: configured in `.daily-curator/config.json`.
- Daily summary: configured in `.daily-curator/config.json`.
- Knowledge card: short retrieval-oriented title.
- MOC/map: topic plus `MOC` or local equivalent.
"""


def default_architecture(config: dict) -> str:
    paths = config["paths"]
    return f"""---
title: Vault Architecture
type: vault-architecture
status: active
---

# Vault Architecture

This file records the curation structure used by `obsidian-daily-curator-generic`.

## Configured folders

- Daily notes: `{paths['daily_notes']}`
- Daily summaries: `{paths['daily_summaries']}`
- Knowledge cards: `{paths['knowledge_cards']}`
- Sources/resources: `{paths['sources']}`
- MOCs/maps: `{paths['mocs']}`
- Projects: `{paths['projects']}`
- Templates: `{paths['templates']}`
- Workbench: `{paths['workbench']}`

## Change log

| Date | Change | Reason |
|---|---|---|
"""


def default_unresolved() -> str:
    return """---
title: Unresolved Curation Queue
type: unresolved-queue
status: active
---

# Unresolved Curation Queue

Use this for ambiguous, unverified, or decision-needed items.

| Date | Source | Item | Reason | Suggested action |
|---|---|---|---|---|
"""


def default_log() -> str:
    return """---
title: Daily Curation Log
type: curation-log
status: active
---

# Daily Curation Log

| Run date | Target date | Sources | Output | Cards | MOC updates | Unresolved | Status |
|---|---|---|---|---:|---:|---:|---|
"""


def quick_capture_template() -> str:
    return """---
title: '{{date}} Quick Capture'
type: quick-capture
date: '{{date}}'
status: raw
tags:
  - type/quick-capture
---

# {{date}} Quick Capture

> Capture with low friction during the day. The curator will classify and distill at the end of the day.

## Context

- Main focus:
- Keywords:

## Ideas

- [idea] 

## Knowledge / concepts

- [knowledge] 

## Code / tools

- [code] 

## Resources / web / tools

- [resource] Title:  
  URL:  
  Why useful:

## News / current info

- [info] Claim:  
  Source:  
  Needs verification: yes / no

## Papers

- [paper] Title:  
  URL / DOI:  
  Useful point:

## Videos / courses / podcasts

- [video] Title:  
  URL:  
  Timestamp:  
  Key point:

## Questions

- [question] 

## Tasks

- [ ] 

## Reflections

- [reflection] 

## Raw paste area

"""


def knowledge_card_template() -> str:
    return """---
title: {{title}}
type: knowledge-card
status: seedling
created: {{date}}
updated: {{date}}
source:
  - {{source}}
tags:
  - type/knowledge-card
---

# {{title}}

## Core idea


## Explanation


## Example


## Source

- {{source}}

## Links

- MOC/map:
- Related notes:

## Review questions

- 
"""


def daily_summary_template() -> str:
    return """---
title: {{date}} Daily Summary
type: daily-summary
date: {{date}}
source:
  - {{source}}
tags:
  - type/daily-summary
---

# {{date}} Daily Summary

## Overview


## Input sources processed


## Knowledge distilled


## Created / updated notes


## Resources, papers, videos, and info


## Ideas and project leads


## Code / tool learnings


## Tasks and questions


## Reflection


## Next steps


## Change log: what went where


"""


def main() -> int:
    args = parse_args()
    vault = Path(args.vault).resolve()
    if not vault.exists():
        raise SystemExit(f"Vault path does not exist: {vault}")

    default_config = load_default_config()
    config_rel = args.config or default_config["paths"]["config"]
    config_path = vault / config_rel

    if config_path.exists():
        existing = json.loads(config_path.read_text(encoding="utf-8"))
        config = deep_merge(default_config, existing)
    else:
        config = default_config

    apply = args.apply
    dry_run = args.dry_run or not apply
    actions: list[tuple[str, Path, str | None]] = []

    paths = config["paths"]
    dirs = [
        paths["workbench"], paths["daily_notes"], paths["templates"],
        paths["daily_summaries"], paths["knowledge_cards"], paths["sources"],
        paths["mocs"], paths["projects"], paths.get("career", "Career"),
    ]
    for d in dict.fromkeys(dirs):
        actions.append(("dir", vault / d, None))

    files = {
        paths["config"]: json.dumps(config, indent=2, ensure_ascii=False) + "\n",
        paths["rules"]: default_rules(config),
        paths["architecture"]: default_architecture(config),
        paths["unresolved"]: default_unresolved(),
        paths["curation_log"]: default_log(),
        paths["quick_capture_template"]: quick_capture_template(),
        paths["knowledge_card_template"]: knowledge_card_template(),
        paths["daily_summary_template"]: daily_summary_template(),
    }
    for f, content in files.items():
        actions.append(("file", vault / f, content))

    print("# Bootstrap plan" + (" (dry run)" if dry_run else ""))
    print(f"- Vault: `{vault}`")
    print(f"- Config: `{config_rel}`")

    for kind, path, content in actions:
        exists = path.exists()
        status = "exists" if exists else "create"
        if exists and args.overwrite and kind == "file":
            status = "overwrite"
        print(f"- {status}: `{rel(path, vault)}`")
        if apply:
            if kind == "dir":
                path.mkdir(parents=True, exist_ok=True)
            else:
                if exists and not args.overwrite:
                    continue
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content or "", encoding="utf-8", newline="\n")

    if dry_run:
        print("\nNo changes written. Re-run with --apply to create missing files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
