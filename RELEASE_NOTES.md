# Release Notes

## public-v0.1 — 2026-05-25

Initial public release of `obsidian-daily-curator-generic`.

### Highlights

- Configurable Obsidian daily-note curation skill.
- Safe first-run bootstrap with `--dry-run` and `--apply` modes.
- Vault-local configuration at `.daily-curator/config.json`.
- Default folders for daily notes, templates, summaries, knowledge cards, sources, maps, projects, and career notes.
- Quick-capture note creation with overwrite protection.
- Read-only scan helper for daily note candidates and same-day modified notes.
- Release smoke tests and release checks.
- Minimal English example vault and Chinese example vault.

### Safety guarantees

- Does not overwrite existing managed files by default.
- Does not bulk move, rename, or delete notes without explicit approval.
- Keeps ambiguous items in the unresolved queue.
- Uses configurable vault-relative paths.

### Known limitations

- This is a skill and helper-script package, not a standalone Obsidian plugin.
- It does not run on a schedule by itself.
- Final curation quality depends on the agent using the skill and the user's vault conventions.
- Automated curation should be used with backups/version history enabled.

### Recommended install

Copy the `obsidian-daily-curator-generic` folder into your agent's skills directory, then initialize each target vault with:

```bash
python scripts/bootstrap_vault.py --vault /path/to/vault --dry-run
python scripts/bootstrap_vault.py --vault /path/to/vault --apply
```
