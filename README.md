# Obsidian Daily Curator Generic

> **Write freely during the day. Let an agent turn the mess into a navigable knowledge base at night.**  
> **白天只管随手记，晚上让 Agent 帮你整理成可复习、可检索、会持续进化的 Obsidian 知识库。**

A configurable agent skill for Obsidian users who collect ideas, learning notes, web clips, papers, videos, code snippets, tasks, and questions throughout the day — but do not want their vault to become a chronological dumping ground.

This skill helps your agent transform messy daily captures into:

- daily summaries that explain **what was learned and where it went**;
- atomic knowledge cards;
- source/resource notes for web clips, papers, videos, and tools;
- MOCs/maps and indexes;
- unresolved queues for ambiguous items;
- tomorrow's quick-capture note.

It is **safe by default**, configurable through `.daily-curator/config.json`, and designed to respect your existing Obsidian vault instead of forcing one rigid structure.

---

## 中文介绍

如果你也有这种问题：

- 每天学了很多东西，但都散落在日记、网页剪藏、论文、视频笔记和代码片段里；
- 白天不想为了“知识库格式”打断学习节奏；
- 收藏了很多资料，但后来很难复习、查找、串联；
- 日记越来越多，但真正沉淀成长期知识的内容很少；
- 想让 Obsidian 知识库自动演化，而不是每隔一段时间手动大扫除。

那么这个 skill 的目标就是：

> **你负责低摩擦记录，Agent 负责日终整理、知识沉淀、链接管理和结构迭代。**

### 它能帮你做什么

每天结束时，让 Agent 运行这个 skill。它会帮助你：

- 扫描当天的 daily note、quick capture 和当天修改过的学习记录；
- 识别并区分：想法、知识点、代码用法、资料、论文、视频、资讯、任务、问题、项目线索和复盘；
- 把可复用知识沉淀为知识卡片；
- 把网页、论文、视频、工具等整理为资料笔记；
- 更新 MOC / map / index；
- 生成一份日终总结，明确记录“什么内容被放到了哪里”；
- 对不确定内容放入 unresolved queue，而不是强行归类；
- 自动准备第二天的 quick-capture 文档。

### 适合谁

- 用 Obsidian 做第二大脑、学习笔记、研究笔记或工作知识库的人；
- 每天会记录大量碎片信息，但不想白天花太多时间整理格式的人；
- 经常导入网页、论文、视频、工具文档、代码片段的人；
- 想要“日记输入 → 知识库沉淀 → 复习查阅”的长期工作流的人；
- 想让 AI agent 辅助整理 vault，但又担心它乱改文件的人。

### 安全原则

这个 skill 默认非常保守：

- 不重写你的原始日记和导入资料；
- 不默认覆盖已有文件；
- 不会在未确认时批量移动、重命名或删除笔记；
- 初始化支持 `--dry-run` 预览；
- 所有路径都通过 `.daily-curator/config.json` 配置；
- 分类不确定的内容会进入 `.daily-curator/unresolved.md`。

> 建议在重要 vault 中使用前，先开启 Git、Obsidian Sync 历史版本或其他备份方式。

---

## English Overview

### The problem

Daily notes are great for capture, but terrible as the final storage layer. Over time, a vault can become a timeline of fragments:

- half-digested web clips;
- copied paper abstracts;
- useful but forgotten code snippets;
- scattered ideas;
- tasks and open questions mixed with learning notes;
- daily logs that are hard to review later.

This skill provides a repeatable end-of-day curation workflow for agent-enabled Obsidian users.

### What it does

At the end of a day, ask your agent to run this skill. It will help:

- scan the target day's daily note and same-day modified learning notes;
- separate ideas, durable knowledge, code snippets, resources, papers, videos, news/info, tasks, questions, projects, and reflections;
- create or update knowledge cards and source notes;
- update MOCs/maps and indexes;
- produce a daily summary that says what went where;
- keep uncertain items in an unresolved queue;
- prepare the next day's quick-capture note.

### Good fit for

- Obsidian users building a second brain;
- students, researchers, engineers, writers, and knowledge workers;
- people who capture first and organize later;
- users who import web pages, papers, videos, docs, and snippets;
- anyone who wants an AI-assisted vault workflow with conservative file safety.

---

## How the workflow feels

During the day, write with minimal friction:

```markdown
- [idea] Retrieval is easier when note titles match how I will search later.
- [knowledge] A MOC should be a navigation layer, not a dumping ground.
- [code] Python pathlib: `Path.mkdir(parents=True, exist_ok=True)` creates nested folders safely.
- [resource] Title: Obsidian Help - Internal links  
  URL: https://help.obsidian.md/links  
  Why useful: explains wikilink behavior.
- [question] Should source notes and knowledge cards use different status fields?
```

At night, ask your agent:

```text
Use obsidian-daily-curator-generic to curate today.
```

The expected output is not just a summary. It should tell you:

- which source notes were processed;
- which knowledge cards were created or updated;
- which resources were saved for later digestion;
- which MOCs/maps were updated;
- which questions or ambiguous items still need attention;
- where tomorrow's quick-capture note was prepared.

---

## Safety model

The skill is intentionally conservative:

- preserves raw daily notes and imported sources;
- does not overwrite existing managed files by default;
- does not bulk move, rename, or delete notes without explicit approval;
- supports dry-run initialization;
- keeps configuration inside the vault at `.daily-curator/config.json`;
- leaves ambiguous items in `.daily-curator/unresolved.md`.

Before first use on an important vault, make sure you have a backup, Git history, Obsidian Sync version history, or another recovery path.

---

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

---

## Installation

Copy this folder into your agent's skills directory.

For Codex-style skills, the final installed path usually looks like:

```text
<skills-dir>/obsidian-daily-curator-generic/SKILL.md
```

If you are developing or reviewing the release package, keep it outside your active skills directory to avoid accidental triggering.

---

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

---

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

---

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

## Examples

See:

- `examples/minimal-vault/` for an English minimal setup.
- `examples/chinese-vault/` for a Chinese-style capture example.

These examples are intentionally small. They show input style and expected curation direction; the actual curation text is generated by the agent at runtime.

---

## What this is not

- It is not an Obsidian plugin.
- It is not a fully autonomous scheduled job.
- It does not replace your judgment about what should become long-term knowledge.
- It does not guarantee factual correctness for current news or high-stakes claims; those should be verified.

Scheduling requires a separate task runner, cron, Windows Task Scheduler, or an agent environment that supports scheduled execution.

---

## Release status

Recommended initial release label: `public-v0.1`.
