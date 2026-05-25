# Obsidian Daily Curator Generic

A configurable agent skill for turning messy Obsidian daily notes, quick captures, imported web clips, papers, videos, code snippets, ideas, tasks, and questions into an evolving knowledge base.

This is the **generic public version**. It does not assume a personal vault layout. It initializes a small configurable workspace in your vault and uses safe defaults.

## What it does

At the end of a day, ask your agent to run this skill. It will help:

- scan the target day's daily note and same-day modified learning notes;
- separate ideas, durable knowledge, code snippets, resources, papers, videos, news/info, tasks, questions, projects, and reflections;
- create or update knowledge cards and source notes;
- update MOCs/maps and indexes;
- produce a daily summary that says what went where;
- keep uncertain items in an unresolved queue;
- prepare the next day's quick-capture note.

## Safety model

The skill is intentionally conservative:

- preserves raw daily notes and imported sources;
- does not overwrite existing managed files by default;
- does not bulk move, rename, or delete notes without explicit approval;
- supports dry-run initialization;
- keeps configuration inside the vault at `.daily-curator/config.json`;
- leaves ambiguous items in `.daily-curator/unresolved.md`.

Before first use on an important vault, make sure you have a backup, Git history, Obsidian Sync version history, or another recovery path.

## Default vault structure

On initialization, the default profile creates only missing folders/files:

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

## Installation

Copy this folder into your agent's skills directory.

For Codex-style skills, the final installed path usually looks like:

```text
<skills-dir>/obsidian-daily-curator-generic/SKILL.md
```

If you are developing or reviewing the release package, keep it outside your active skills directory to avoid accidental triggering.

## First-time setup

From your Obsidian vault root, preview initialization:

```bash
python /path/to/obsidian-daily-curator-generic/scripts/bootstrap_vault.py --vault . --dry-run
```

If the plan looks good, apply it:

```bash
python /path/to/obsidian-daily-curator-generic/scripts/bootstrap_vault.py --vault . --apply
```

The bootstrap script creates missing files/folders and skips existing files unless `--overwrite` is explicitly passed.

## Daily use

During the day, write anything into your daily quick-capture note. Low-friction input is expected.

Useful optional prefixes:

```markdown
- [idea] A thought, hypothesis, analogy, or project angle
- [knowledge] A concept, principle, method, or mental model
- [code] A programming/API usage pattern or debugging lesson
- [resource] A web page, book, tool, dataset, or documentation link
- [info] A current factual claim or news item
- [paper] A paper or research note
- [video] A course, talk, podcast, lecture, or tutorial
- [question] An open question or confusion
- [reflection] A personal lesson or review note
```

Then ask your agent:

```text
Use obsidian-daily-curator-generic to curate today.
```

or:

```text
Run a daily curation for 2026-01-02.
```

## Helpful scripts

### Bootstrap a vault

```bash
python scripts/bootstrap_vault.py --vault /path/to/vault --dry-run
python scripts/bootstrap_vault.py --vault /path/to/vault --apply
```

### Prepare a quick-capture note

```bash
python scripts/prepare_quick_capture.py --vault /path/to/vault --date 2026-01-02
python scripts/prepare_quick_capture.py --vault /path/to/vault --tomorrow
```

### Scan curation context

```bash
python scripts/scan_vault.py --vault /path/to/vault --date 2026-01-02
```

### Run smoke tests

```bash
python scripts/test_smoke.py
```

### Run release checks

```bash
python scripts/check_release.py
```

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

## Examples

See:

- `examples/minimal-vault/` for an English minimal setup.
- `examples/chinese-vault/` for a Chinese-style capture example.

These examples are intentionally small. They show input style and expected curation direction; the actual curation text is generated by the agent at runtime.

## Release status

Recommended initial release label: `public-v0.1`.

This is a skill plus helper scripts, not a fully autonomous scheduled job. Scheduling requires a separate task runner, cron, Windows Task Scheduler, or an agent environment that supports scheduled execution.
