---
name: obsidian-daily-curator-generic
description: Generic, configurable Obsidian daily-note curator for turning messy daily notes, quick captures, learning logs, imported web clips, papers, videos, code snippets, ideas, tasks, and questions into summaries, knowledge cards, source notes, MOCs/maps, and an evolving vault structure. Use when the user wants daily curation, end-of-day review, quick-capture preparation, vault initialization, or safe knowledge-base organization without assuming a fixed personal vault layout.
---

# Obsidian Daily Curator Generic

Curate one day's messy Obsidian input into durable knowledge while respecting the user's existing vault structure. This is the public/generic version: it is configurable, layout-agnostic, and safe by default.

## Core safety rules

- Treat the current working directory as the vault root unless the user gives another path.
- Use vault-relative paths in notes and responses.
- Do not assume a fixed folder layout. Read `.daily-curator/config.json` first.
- If config is missing, bootstrap with a dry run before creating files unless the user explicitly asks to initialize/apply.
- Never overwrite existing notes or templates unless the user explicitly asks.
- Preserve raw daily notes and imported material. Write summaries, cards, and indexes separately.
- Do not bulk move, rename, or delete notes without explicit approval.
- If classification is uncertain, put the item in the configured unresolved file.
- Keep permanent workflow state in the vault config/log files, not in conversation memory.
- For time-sensitive, legal, medical, financial, or factual news claims, verify with browsing when required by higher-level instructions; otherwise mark as unverified.

## Script path convention

Resolve script paths relative to this skill directory. In examples below, replace `<skill-dir>` with the folder containing this `SKILL.md`.

## First-time initialization

1. Check whether `.daily-curator/config.json` exists.
2. If missing, run a dry run:

```powershell
python "<skill-dir>/scripts/bootstrap_vault.py" --vault . --dry-run
```

3. Show the planned files/folders to the user.
4. If the user approves or explicitly asked to initialize, run:

```powershell
python "<skill-dir>/scripts/bootstrap_vault.py" --vault . --apply
```

The bootstrap script creates only missing files and never overwrites by default.

## Configuration

Default config path: `.daily-curator/config.json`.

The config controls:

- daily note folder and filename pattern
- templates folder
- knowledge card folder
- source/resource folder
- MOC/map folder
- project folder
- review/summary folder
- unresolved queue
- curation log
- folders to include/exclude during scans
- whether to prepare the next day's note

If the user already has a vault structure, edit the config rather than changing the skill.

## Target date resolution

1. If the user names a date, use that date.
2. If the user says today, get the actual local date from the shell; do not rely on model memory.
3. If the user says yesterday, calculate it from the actual local date.
4. If no date is specified, default to today.

Use `YYYY-MM-DD` for generated filenames and log entries unless the config says otherwise.

## Daily curation workflow

### 1. Scan the vault

Run:

```powershell
python "<skill-dir>/scripts/scan_vault.py" --vault . --date YYYY-MM-DD
```

Use the output to identify:

- config and template status
- daily note candidates
- notes modified on the target date
- imported source notes likely created that day
- existing MOCs/maps and folders

### 2. Intake source material

Collect content from:

1. The current editor selection or current note if provided.
2. The configured daily note for the target date.
3. Quick-capture notes matching the target date.
4. Notes modified on the target date in configured scan folders.
5. Imported web clips, source notes, papers, videos, PDFs, and tool notes created or modified on the target date.
6. Unresolved queue entries referencing the target date.

If no source note can be found, report that clearly and do not create empty summaries.

### 3. Analyze before writing

Before creating or updating notes:

- Identify distinct items even if the input is unordered.
- Separate the user's own ideas from copied/imported source material.
- Separate durable knowledge from one-off information.
- Detect whether code snippets are reusable patterns, debugging notes, or project-specific implementation details.
- Detect whether imported resources are merely saved, partially understood, or ready to be distilled.
- Search existing knowledge cards and MOCs/maps before creating new categories.

### 4. Item taxonomy

Use these item types:

- `idea`: user's own idea, hypothesis, analogy, product angle, writing angle.
- `knowledge`: reusable concept, principle, method, mental model, technical point.
- `code`: programming usage, command, snippet, API pattern, debugging lesson.
- `resource`: article, book, documentation, tool, website, dataset, general source.
- `paper`: academic paper or research note.
- `video`: course, lecture, talk, podcast, tutorial.
- `info`: news, market/industry update, current event, factual claim.
- `task`: actionable todo, follow-up, reminder.
- `question`: confusion, open question, research direction.
- `project`: project idea, implementation note, product/design decision.
- `career`: resume, interview, job-search, networking, career planning.
- `reflection`: personal lesson, decision, emotion, pattern, review.

For each item, keep a source backlink and, when useful, a short source excerpt.

### 5. Classify and write

Use the configured paths. Default behavior:

- `knowledge` -> knowledge cards.
- `code` -> reusable knowledge card if generally useful; project note if project-specific.
- `resource` / `paper` / `video` -> source/resource note; distill durable claims into knowledge cards only when understood.
- `info` -> source note or daily summary; mark current facts as unverified unless checked.
- `idea` -> daily summary, project note, or knowledge card if reusable.
- `project` -> project folder or unresolved queue if project is not established.
- `career` -> career folder if configured, otherwise unresolved queue or daily summary.
- `reflection` -> daily summary.
- `task` / `question` -> daily summary plus unresolved queue when follow-up is needed.

Knowledge cards should be atomic: one concept or claim cluster per note. Prefer updating an existing card over creating a duplicate.

### 6. Update MOCs/maps and indexes

For each created or materially updated card/resource:

1. Find the closest existing MOC/map.
2. Add a wikilink under the most relevant heading.
3. If no MOC/map fits and the theme is likely to recur, create a new MOC/map in the configured MOC folder.
4. If unsure, add the ambiguity to the unresolved queue instead of inventing a category.

### 7. Evolve architecture carefully

Update the configured architecture/rules note only for real structure changes, such as:

- New recurring topic folder or MOC/map.
- Repeated unresolved items showing a missing category.
- A folder becoming overloaded or semantically mixed.
- A naming/tagging convention that needs to become explicit.
- A new recurring capture type such as code snippets, web clips, papers, or video digests.

For major restructuring, propose the change before applying it.

### 8. Produce daily summary

Create or update the configured daily summary note for the target date.

Include:

- overview
- input sources processed
- key knowledge distilled
- created/updated knowledge cards
- resources, papers, videos, and info items
- ideas and project leads
- code/programming learnings
- tasks and questions
- reflection
- suggested next steps
- change log: explicitly state what went where using wikilinks

### 9. Log the run

Append to the configured curation log:

- target date
- source notes
- summary note
- number of cards/resources/MOC updates
- unresolved item count
- status

If the same date was already processed, log an incremental run and mention what changed.

### 10. Prepare the next day's quick-capture note

If config `behavior.prepare_next_day_note` is true, create the next day's note unless it already exists:

```powershell
python "<skill-dir>/scripts/prepare_quick_capture.py" --vault . --date NEXT-DATE
```

Mention the prepared note in the final response.

### 11. Verify before responding

Before saying the work is done:

- Confirm generated/updated files exist.
- Check obvious wikilinks point to existing notes when you created them.
- Ensure frontmatter delimiters are balanced.
- Avoid duplicate notes for the same concept.
- Report changed files as clickable wikilinks.

## Final response format

Respond concisely with:

1. Target date and source notes processed.
2. Created/updated notes as wikilinks.
3. Routing summary: knowledge/resources/ideas/code/tasks went where.
4. Prepared next quick-capture note, if enabled.
5. Items left in the unresolved queue.
6. Architecture changes applied or proposed.
