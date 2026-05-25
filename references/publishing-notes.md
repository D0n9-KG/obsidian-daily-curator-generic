# Publishing notes

This generic skill is designed for distribution:

- No user-specific absolute paths.
- No fixed personal vault layout.
- Uses `.daily-curator/config.json` for paths and behavior.
- Includes dry-run bootstrap.
- Scripts never overwrite by default.
- Defaults are English and can be edited in config.

## Pre-release checklist

Run from the release package root:

```bash
python scripts/test_smoke.py
python scripts/check_release.py
```

Check manually:

- README explains installation and first run.
- Dry-run behavior is clear.
- No private paths or personal vault names appear in files.
- Examples are small and non-sensitive.
- Version label is set in the release notes.

Recommended initial release label: `public-v0.1` until tested on multiple vaults.
