# Obsidian Daily Curator Generic

[English](README.md) · [简体中文](README.zh-CN.md)

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Release](https://img.shields.io/badge/release-public--v0.1-blue)
![Obsidian](https://img.shields.io/badge/Obsidian-Markdown-purple)
![Safety](https://img.shields.io/badge/safety-dry--run%20first-orange)

> **Capture freely during the day. Let an agent turn the mess into a navigable Obsidian knowledge base at night.**

Obsidian Daily Curator Generic is a configurable agent skill for people who collect ideas, learning notes, web clips, papers, videos, code snippets, tasks, and questions throughout the day — but do not want their vault to become a chronological dumping ground.

It gives your agent a repeatable end-of-day workflow for turning raw daily capture into summaries, knowledge cards, source notes, MOCs/maps, unresolved queues, and tomorrow's quick-capture note.

---

## Why this exists

Daily notes are excellent for capture, but poor as the final storage layer.

Without curation, a vault slowly turns into:

- half-digested web clips;
- copied paper abstracts;
- useful but forgotten code snippets;
- scattered ideas with no retrieval path;
- tasks and questions mixed into learning notes;
- daily logs that are hard to review later.

This skill is designed around a simple workflow:

```text
messy daily capture → end-of-day agent curation → durable knowledge base
```

You keep learning without interrupting yourself for perfect formatting. Your agent handles the nightly organization pass.

---

## What it produces

| Input captured during the day | Curated output |
|---|---|
| Ideas and hypotheses | Daily summary, project leads, or reusable notes |
| Concepts and methods | Atomic knowledge cards |
| Python/API/code snippets | Reusable code-pattern notes or project notes |
| Web clips, docs, tools | Source/resource notes |
| Papers and videos | Source notes plus distilled knowledge cards |
| News/current info | Source notes or summary items marked unverified when needed |
| Tasks and open questions | Daily summary and unresolved queue |
| Reflections | Daily review and lessons learned |

A good curation run should tell you **what was learned, what was created, and where everything went**.


---

## Recommended Obsidian setup

You can use this skill with plain Markdown files, but the workflow is smoother if Obsidian is configured for daily capture, templates, links, and recovery.

### Minimum recommended core plugins

Enable these built-in Obsidian core plugins:

| Plugin | Why it helps |
|---|---|
| **Daily notes** | One-click access to today's capture note. |
| **Templates** | Insert or maintain reusable daily/source/card templates. |
| **Backlinks** | See which notes point to a card, source, or daily note. |
| **Outgoing links** | Find unlinked mentions and missing links while reviewing notes. |
| **Search** | Quickly locate prior cards before creating duplicates. |
| **Quick switcher** | Open notes and MOCs/maps without browsing folders. |
| **Properties view** | Inspect and clean up metadata such as `type`, `status`, `source`, and `date`. |
| **File recovery** | Provides an extra safety net while experimenting with agent-assisted workflows. |

### Recommended settings

After running `bootstrap_vault.py --apply`, align Obsidian with the generated config:

| Area | Suggested setting |
|---|---|
| **Daily notes > New file location** | Same as `paths.daily_notes` in `.daily-curator/config.json` (default: `Daily`). |
| **Daily notes > Date format** | `YYYY-MM-DD` unless you changed `naming.daily_note`. |
| **Daily notes > Template file location** | The generated quick-capture template, default `Templates/Quick Capture Template.md`. |
| **Templates > Template folder location** | Same as `paths.templates` (default: `Templates`). |
| **Properties** | Use consistent fields such as `type`, `status`, `date`, `source`, and `tags`. |
| **Backups** | Keep File Recovery, Git, Obsidian Sync version history, or another backup method enabled. |

### For web clips and imported sources

If you often save web pages, articles, documentation, or tools, install and configure **Obsidian Web Clipper**.

Recommended Web Clipper behavior:

- save raw clips into the configured source folder, default `Sources`; or
- append quick snippets to the current daily note when you want everything in one capture stream;
- include at least `title`, `url`, `source`, and `created` metadata;
- mark undigested clips as `status: to-process` or similar.

This keeps raw source material separate from distilled knowledge cards.

### Optional community plugins

These are not required. Add them only if they already fit your workflow:

| Plugin | Use when |
|---|---|
| **Dataview** | You want dashboards for unresolved items, review queues, source notes, or knowledge cards. |
| **Tasks** | You manage actionable tasks inside Obsidian. |
| **Templater** | You need advanced dynamic templates beyond the core Templates plugin. |
| **QuickAdd** | You want command-driven capture menus or faster manual capture. |
| **Periodic Notes** | You also maintain weekly/monthly/quarterly reviews. |

Start with the core plugins first. The skill is designed to work without requiring any community plugin.


## Quick start

### 1. Install the skill

Copy this folder into your agent's skills directory:

```text
<skills-dir>/obsidian-daily-curator-generic/SKILL.md
```

If you are reviewing or developing this package, keep it outside your active skills directory to avoid accidental triggering.

### 2. Initialize a vault safely

From your Obsidian vault root, preview the setup first:

```bash
python /path/to/obsidian-daily-curator-generic/scripts/bootstrap_vault.py --vault . --dry-run
```

If the plan looks good, apply it:

```bash
python /path/to/obsidian-daily-curator-generic/scripts/bootstrap_vault.py --vault . --apply
```

### 3. Capture during the day

Write messy notes freely. Optional prefixes help the agent classify faster:

```markdown
- [idea] Retrieval works better when note titles match how I will search later.
- [knowledge] A MOC should be a navigation layer, not a dumping ground.
- [code] Python pathlib: `Path.mkdir(parents=True, exist_ok=True)` creates nested folders safely.
- [resource] Title: Obsidian Help - Internal links  
  URL: https://help.obsidian.md/links  
  Why useful: explains wikilink behavior.
- [question] Should source notes and knowledge cards use different status fields?
```

### 4. Curate at night

Ask your agent:

```text
Use obsidian-daily-curator-generic to curate today.
```

or:

```text
Run a daily curation for 2026-01-02.
```

---

## Safety model

This skill is intentionally conservative:

- preserves raw daily notes and imported sources;
- does not overwrite existing managed files by default;
- does not bulk move, rename, or delete notes without explicit approval;
- supports dry-run initialization;
- keeps configuration inside the vault at `.daily-curator/config.json`;
- leaves ambiguous items in `.daily-curator/unresolved.md`.

Before using it on an important vault, enable Git, Obsidian Sync version history, or another backup/recovery path.

---

## Default vault structure

The bootstrap script creates only missing folders/files:

```text
.daily-curator/
  config.json
  curation-rules.md
  vault-architecture.md
  unresolved.md
  curation-log.md
Daily/
Templates/
Reviews/Daily/
Knowledge/
Sources/
Maps/
Projects/
Career/
```

You can change all of these paths in `.daily-curator/config.json`.

---

## Configuration

Edit `.daily-curator/config.json` after bootstrap.

Important fields:

- `paths.daily_notes`: where quick-capture/daily notes live.
- `paths.knowledge_cards`: where durable knowledge cards are written.
- `paths.sources`: where web clips, papers, videos, and resources are tracked.
- `paths.mocs`: where maps/MOCs live.
- `paths.daily_summaries`: where daily summaries are written.
- `paths.unresolved`: where uncertain items go.
- `scan.include_dirs`: restrict scanning to selected folders. Empty means scan the vault except excluded folders.
- `scan.exclude_dirs`: folders ignored by the scanner.
- `behavior.prepare_next_day_note`: whether to create tomorrow's quick-capture note after curation.
- `behavior.bulk_move_requires_approval`: keep this true unless you really know what you are doing.

---

## Helper scripts

```bash
# Preview or initialize a vault
python scripts/bootstrap_vault.py --vault /path/to/vault --dry-run
python scripts/bootstrap_vault.py --vault /path/to/vault --apply

# Prepare a daily quick-capture note
python scripts/prepare_quick_capture.py --vault /path/to/vault --date 2026-01-02
python scripts/prepare_quick_capture.py --vault /path/to/vault --tomorrow

# Scan curation context
python scripts/scan_vault.py --vault /path/to/vault --date 2026-01-02

# Validate the release package
python scripts/test_smoke.py
python scripts/check_release.py
```

---

## Examples

- `examples/minimal-vault/` — minimal English example.
- `examples/chinese-vault/` — Chinese quick-capture example.

The examples show input style and expected curation direction. The actual curation text is generated by the agent at runtime.

---

## What this is not

- Not an Obsidian plugin.
- Not a fully autonomous scheduled job.
- Not a replacement for your judgment about what deserves long-term storage.
- Not a factual verification engine for current news or high-stakes claims.

Scheduling requires a separate task runner, cron, Windows Task Scheduler, or an agent environment that supports scheduled execution.

---

## Project status

Current release: `public-v0.1`

This is an early public version. It is designed to be safe and configurable, but should be tested on a backed-up vault before serious use.

## License

MIT
