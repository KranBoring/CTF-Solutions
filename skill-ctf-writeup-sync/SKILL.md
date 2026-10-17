---
name: ctf-writeup-sync
description: Manage this CTF repository's write-up indexes and create new website challenge folders when the user says "Cập nhập wu" or "Tạo folder web ...".
---

# CTF repository workflow

This skill applies only inside the CTF repository. Read the repository root `AGENTS.md` before acting; it is the authoritative workflow and takes precedence over this file. Follow its naming, ordering, URL, validation, and safety rules exactly.

## Triggers

- When the user says `Cập nhập wu`, execute the complete write-up synchronization procedure in `AGENTS.md`.
- When the user says `Tạo folder web ...`, execute the website and difficulty folder creation procedure in `AGENTS.md`, including the requested priority order.

Do not use a generic or old standalone synchronizer as a substitute for `AGENTS.md`: challenge names, nested layouts, CryptoHack course references, tables with extra columns, and `Others-Events` require repository-aware handling. Preserve existing content and report ambiguous mappings before changing them.

## Stable execution

- Read the repository `AGENTS.md` before touching files. Treat existing user changes as protected.
- For ordinary table/index synchronization, use `scripts/sync_writeups.py --dry-run <repo-root>` first. Review its unresolved and ambiguous mappings; never resolve them with fuzzy matching.
- Run the same command without `--dry-run` only after the preview shows the intended scope. The helper edits only detected write-up cells and progress suffixes, and writes files through an atomic replacement.
- The helper is not a replacement for the CryptoHack Course rules or the `Others-Events` table-creation rules in `AGENTS.md`; handle those cases explicitly and verify the resulting diff.
- After every run, inspect `git diff --check`, the changed README rows, and all unresolved mappings. If a parser would rewrite unrelated columns, line endings, URLs, IDs, or labels, stop and restore that file before continuing.
