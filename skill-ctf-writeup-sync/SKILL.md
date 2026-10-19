---
name: ctf-writeup-sync
description: Update CTF write-up indexes and progress, or create challenge folders for a new website.
---

# CTF repository workflow

Use this skill only in CTF-Solutions. The repository-root `AGENTS.md` is authoritative; consult only the section for the requested task instead of restating or copying its full procedure into the conversation.

## `Cập nhập wu`

1. Run `python3 skill-ctf-writeup-sync/scripts/sync_writeups.py --dry-run <repo-root>` (on Windows, use Ubuntu WSL).
2. Review its proposed counts and unresolved/ambiguous rows. Exact normalized names, explicit valid write-up links, final URL slugs, and approved `challenge-aliases.csv` entries are the only mapping evidence. Do not guess; the helper skips uncertain rows.
3. If the preview is in scope, run the same command without `--dry-run`.
4. Verify with `git diff --check`, a second dry-run (the proposed change count should be zero; unresolved rows may remain), and `python3 -m unittest discover -s skill-ctf-writeup-sync/tests`. Report unresolved mappings; do not claim full sync if any remain.

The helper performs deterministic parsing and writes atomically; do not load its source into context unless debugging. It preserves challenge URLs and unrelated columns. CryptoHack Course and `Others-Events` creation rules remain governed by `AGENTS.md`.

## `Tạo folder web ...`

Follow the website-creation procedure in `AGENTS.md`. Use the official/user-provided challenge list, then invoke `autocreatemyfolder "<original challenge name>"` in WSL from each category directory. Never guess blocked/hidden entries or overwrite an existing challenge folder.
