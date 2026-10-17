#!/usr/bin/env python3
"""Synchronize challenge README status cells using exact, auditable mappings."""
from __future__ import annotations

import argparse
import html
import os
import re
import tempfile
import unicodedata
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

NAME_HEADERS = {"challenge", "name", "exercise", "bài"}
STATUS_HEADERS = {"writeup", "solution", "writeupstatus"}
ID_HEADERS = {"id", "#", "no", "number", "challengeid"}
PLACEHOLDERS = {"todo", "tbd", "chưa có write-up", "coming soon", "write-up coming soon"}


def norm(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(c for c in value if not unicodedata.combining(c)).casefold()
    return "".join(c for c in value if c.isalnum())


def meaningful(path: Path) -> bool:
    # Decode errors are deliberately propagated; they must never become "empty".
    value = path.read_text(encoding="utf-8-sig")
    value = re.sub(r"<!--.*?-->", "", value, flags=re.S)
    remaining = []
    for line in value.splitlines():
        line = line.strip()
        if not line or re.fullmatch(r"#{1,6}(?:\s+.*)?", line):
            continue
        if re.fullmatch(r"(?:TODO|TBD|Chưa có write-up|Coming soon|Write-up coming soon)[.:]?", line, re.I):
            continue
        remaining.append(line)
    return bool("".join(remaining).strip())


def splitrow(line: str) -> list[str]:
    value = line.rstrip("\r\n")
    start, end = (1 if value.startswith("|") else 0), len(value) - (1 if value.endswith("|") else 0)
    cells, cell_start, escaped = [], start, False
    for i in range(start, end):
        char = value[i]
        if char == "|" and not escaped:
            cells.append(value[cell_start:i])
            cell_start = i + 1
        if char == "\\":
            escaped = not escaped
        else:
            escaped = False
    cells.append(value[cell_start:end])
    return cells


def header_key(cell: str) -> str:
    value = re.sub(r"<[^>]*>", "", cell).strip().strip("`*_").casefold()
    return re.sub(r"[\s_-]+", "", value)


def is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r"\s*:?-+:?\s*", cell) for cell in cells)


def challenge_label(cell: str) -> str:
    # A link label is the challenge name; its URL is evidence only in the URL fallback.
    match = re.search(r"\[((?:\\.|[^]])*)\]\((?:<[^>]*>|[^)]*)\)", cell)
    value = match.group(1) if match else cell
    value = re.sub(r"<[^>]*>|`", "", value)
    return html.unescape(value.replace(r"\|", "|")).strip()


def internal_writeup_link(cell: str, readme_dir: Path, root: Path) -> tuple[Path | None, bool]:
    """Return (resolved path, saw write-up link); reject escaping/broken targets."""
    for match in re.finditer(r"\[[^]]*\]\((?:<([^>]+)>|([^\s)]*))\)", cell):
        target = match.group(1) or match.group(2)
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path.lower().endswith("write-up.md"):
            continue
        path = (readme_dir / unquote(parsed.path)).resolve()
        try:
            path.relative_to(root)
        except ValueError:
            return None, True
        return (path if path.is_file() else None), True
    return None, False


def candidate_dirs(base: Path, root: Path) -> list[Path]:
    base = base.resolve()
    found = []
    for writeup in base.rglob("write-up.md"):
        if not writeup.is_file() or any(part in {".git", "skill-ctf-writeup-sync"} for part in writeup.relative_to(root).parts):
            continue
        found.append(writeup.parent.resolve())
    return found


def map_candidate(label: str, cell: str, base: Path, root: Path) -> tuple[Path | None, list[Path], str]:
    candidates = candidate_dirs(base, root)
    exact = [path for path in candidates if norm(path.name) == norm(label)]
    if exact:
        return (exact[0] if len(exact) == 1 else None), exact, "exact name"
    # Only the final URL path segment may provide the fallback match.
    url = re.search(r"\]\((?:<)?(https?://[^)>]+)", cell)
    if url:
        segment = unquote(urlsplit(url.group(1)).path.rstrip("/").split("/")[-1])
        matched = [path for path in candidates if norm(path.name) == norm(segment)]
        if matched:
            return (matched[0] if len(matched) == 1 else None), matched, "URL segment"
    return None, [], "no exact match"


def relative_link(path: Path, base: Path) -> str:
    rel = os.path.relpath(path, base).replace(os.sep, "/")
    return quote(rel, safe="/.-_~")


def atomic_write(path: Path, value: str) -> None:
    fd, temp = tempfile.mkstemp(dir=path.parent, prefix="." + path.name + ".")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as stream:
            stream.write(value)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def status_is_external(cell: str) -> bool:
    return any(urlsplit(m.group(1) or m.group(2)).scheme in {"http", "https"}
               for m in re.finditer(r"\[[^]]*\]\((?:<([^>]+)>|([^\s)]*))\)", cell))


def table_rows(readme: Path) -> list[tuple[str, str]]:
    """Return (challenge label, status cell) for every recognized table row."""
    lines = readme.read_text(encoding="utf-8-sig").splitlines()
    rows: list[tuple[str, str]] = []
    for i in range(len(lines) - 1):
        header, divider = splitrow(lines[i]), splitrow(lines[i + 1])
        if not is_separator(divider) or len(header) != len(divider):
            continue
        keys = [header_key(cell) for cell in header]
        names = [j for j, key in enumerate(keys) if key in NAME_HEADERS]
        statuses = [j for j, key in enumerate(keys) if key in STATUS_HEADERS]
        if len(names) != 1 or len(statuses) != 1:
            continue
        j = i + 2
        while j < len(lines) and lines[j].strip() and "|" in lines[j]:
            cells = splitrow(lines[j])
            if len(cells) != len(header) or is_separator(cells):
                break
            rows.append((challenge_label(cells[names[0]]), cells[statuses[0]]))
            j += 1
    return rows


def course_status(label: str, readme: Path, root: Path) -> str | None:
    """Return an unambiguous CryptoHack Course status for a challenge row."""
    if "Cryptohack/Challenges" not in readme.as_posix():
        return None
    courses = []
    for course in (root / "Cryptohack" / "Course").rglob("README.md"):
        matches = [status for name, status in table_rows(course) if norm(name) == norm(label)]
        if matches:
            courses.append((course, matches[0]))
    if len(courses) != 1:
        return None
    course, _ = courses[0]
    title = next((line.lstrip("# ").strip() for line in course.read_text(encoding="utf-8-sig").splitlines() if line.startswith("#")), course.parent.name)
    return f"Đang nằm ở course [{title}]({relative_link(course, readme.parent)})"


def course_complete(status: str, label: str, readme: Path, root: Path) -> bool:
    match = re.search(r"\[[^]]+\]\((?:<([^>]+)>|([^\s)]*README\.md))\)", status)
    if not match:
        return False
    target = (readme.parent / unquote(match.group(1) or match.group(2))).resolve()
    try:
        target.relative_to(root)
    except ValueError:
        return False
    for name, course_cell in table_rows(target):
        if norm(name) != norm(label):
            continue
        dest, linked = internal_writeup_link(course_cell, target.parent, root)
        if linked and dest:
            try:
                return meaningful(dest)
            except (OSError, UnicodeError):
                return False
        return status_is_external(course_cell)
    return False


def create_others_event_table(readme: Path, root: Path, dry: bool) -> bool:
    """Create the required table for an event README that has challenge folders."""
    if "Others-Events" not in readme.relative_to(root).parts:
        return False
    if table_rows(readme):
        return False
    folders = []
    for marker in ("write-up.md", "solve.py"):
        for path in readme.parent.rglob(marker):
            if any(part in {".git", "skill-ctf-writeup-sync"} for part in path.relative_to(root).parts):
                continue
            folder = path.parent
            if (folder / "README.md").exists() and folder != readme.parent:
                continue
            if folder not in folders:
                folders.append(folder)
    if not folders:
        return False
    rows = ["", "| Challenge | Write-up |", "| --- | --- |"]
    for folder in sorted(folders):
        writeup = folder / "write-up.md"
        if writeup.is_file():
            try:
                done = meaningful(writeup)
            except (OSError, UnicodeError):
                done = False
        else:
            done = False
        status = f"[Đọc write-up]({relative_link(writeup, readme.parent)})" if done else "Chưa có write-up"
        rows.append(f"| {folder.name} | {status} |")
    if not dry:
        original = readme.read_text(encoding="utf-8")
        atomic_write(readme, original.rstrip("\n") + "\n" + "\n".join(rows) + "\n")
    return True


def process(readme: Path, root: Path, dry: bool) -> tuple[int, int, list[str], bool]:
    text = readme.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    total = done = table_count = 0
    issues: list[str] = []
    changed = False
    i = 0
    while i + 1 < len(lines):
        header, divider = splitrow(lines[i]), splitrow(lines[i + 1])
        if not is_separator(divider) or len(header) != len(divider):
            i += 1
            continue
        keys = [header_key(cell) for cell in header]
        names = [j for j, key in enumerate(keys) if key in NAME_HEADERS]
        statuses = [j for j, key in enumerate(keys) if key in STATUS_HEADERS]
        ids = [j for j, key in enumerate(keys) if key in ID_HEADERS]
        if len(names) != 1 or len(statuses) != 1:
            # Ignore unrelated tables. A table that declares a relevant column but
            # cannot identify both required columns is surfaced for manual review.
            if any(key in NAME_HEADERS | STATUS_HEADERS for key in keys):
                issues.append(f"{readme.relative_to(root)}: unclear challenge/status table header")
            i += 1
            continue
        table_count += 1
        name_col, status_col = names[0], statuses[0]
        j = i + 2
        while j < len(lines) and lines[j].strip() and "|" in lines[j]:
            cells = splitrow(lines[j])
            if len(cells) != len(header) or is_separator(cells):
                break
            total += 1
            label = challenge_label(cells[name_col])
            ident = cells[ids[0]].strip() if len(ids) == 1 else ""
            status = cells[status_col]
            course_linked = False
            if status.strip().casefold() in {"chưa có write-up", "todo", "tbd"}:
                linked_course = course_status(label, readme, root)
                if linked_course:
                    status = linked_course
                    cells[status_col] = status
                    changed = True
                    course_linked = True
            if status.lstrip().startswith("Đang nằm ở course"):
                course_linked = True
                if course_complete(status, label, readme, root):
                    done += 1
                desired = status
                if cells[status_col] != desired:
                    cells[status_col] = desired
                    changed = True
                j += 1
                continue
            dest, saw_link = internal_writeup_link(status, readme.parent, root)
            if saw_link and dest is None:
                issues.append(f"{readme.relative_to(root)}: {ident + ' ' if ident else ''}{label}: broken/out-of-repository write-up link")
                j += 1
                continue
            if dest is not None and dest.is_file():
                dest = dest
            elif dest is not None:
                dest = dest / "write-up.md"
            ambiguous: list[Path] = []
            if dest is None and not status_is_external(status):
                dest, ambiguous, evidence = map_candidate(label, cells[name_col], readme.parent, root)
                if dest is not None:
                    dest = dest / "write-up.md"
                if len(ambiguous) > 1:
                    choices = ", ".join(p.relative_to(readme.parent).as_posix() for p in ambiguous)
                    issues.append(f"{readme.relative_to(root)}: {ident + ' ' if ident else ''}{label}: ambiguous ({choices})")
                elif dest is None:
                    issues.append(f"{readme.relative_to(root)}: {ident + ' ' if ident else ''}{label}: unmapped")
            if dest is not None:
                try:
                    has_content = meaningful(dest)
                except (OSError, UnicodeError) as error:
                    issues.append(f"{readme.relative_to(root)}: {label}: cannot read {dest.relative_to(root)}/write-up.md: {error}")
                    j += 1
                    continue
                desired = f" [Đọc write-up]({relative_link(dest, readme.parent)}) " if has_content else " Chưa có write-up "
                if has_content:
                    # Ensure the generated link resolves to the intended file.
                    if (readme.parent / unquote(relative_link(dest, readme.parent))).resolve() != dest.resolve():
                        issues.append(f"{readme.relative_to(root)}: {label}: generated link failed validation")
                        j += 1
                        continue
                    done += 1
                elif status_is_external(status):
                    desired = status
            else:
                # Preserve non-empty external or special status cells. Never erase
                # information simply because an exact local mapping is unavailable.
                desired = status
            if cells[status_col] != desired:
                cells[status_col] = desired
                ending = "\r\n" if lines[j].endswith("\r\n") else "\n" if lines[j].endswith("\n") else ""
                lines[j] = "|" + "|".join(cells) + "|" + ending
                changed = True
            j += 1
        i = j if j > i + 1 else i + 1
    if changed and not dry:
        atomic_write(readme, "".join(lines))
    return done, total, issues, changed


def row_completion(readme: Path, root: Path) -> tuple[int, int]:
    """Count completed rows from the current README contents."""
    lines = readme.read_text(encoding="utf-8").splitlines()
    complete = total = 0
    for i in range(len(lines) - 1):
        header, divider = splitrow(lines[i]), splitrow(lines[i + 1])
        if not is_separator(divider) or len(header) != len(divider):
            continue
        keys = [header_key(cell) for cell in header]
        names = [j for j, key in enumerate(keys) if key in NAME_HEADERS]
        statuses = [j for j, key in enumerate(keys) if key in STATUS_HEADERS]
        if len(names) != 1 or len(statuses) != 1:
            continue
        j = i + 2
        while j < len(lines) and lines[j].strip() and "|" in lines[j]:
            cells = splitrow(lines[j])
            if len(cells) != len(header) or is_separator(cells):
                break
            total += 1
            status = cells[statuses[0]]
            label = challenge_label(cells[names[0]])
            if status.lstrip().startswith("Đang nằm ở course"):
                complete += int(course_complete(status, label, readme, root))
                j += 1
                continue
            dest, linked = internal_writeup_link(status, readme.parent, root)
            if linked:
                if dest:
                    try:
                        complete += int(meaningful(dest))
                    except (OSError, UnicodeError):
                        pass
            elif status_is_external(status):
                complete += 1
            j += 1
    return complete, total


def update_progress(root: Path, dry: bool) -> int:
    pattern = re.compile(r"(\]\()([^)]*README\.md)(\))\s*\(\s*\d+\s*/\s*\d+\s*\)")
    updated = 0
    for readme in root.rglob("README.md"):
        if any(part in {".git", "skill-ctf-writeup-sync"} for part in readme.relative_to(root).parts):
            continue
        text = readme.read_text(encoding="utf-8")
        def replace(match: re.Match[str]) -> str:
            nonlocal updated
            target = (readme.parent / unquote(match.group(2))).resolve()
            try:
                target.relative_to(root)
            except ValueError:
                return match.group(0)
            if not target.is_file():
                return match.group(0)
            complete, total = row_completion(target, root)
            updated += int(match.group(0) != f"{match.group(1)}{match.group(2)}{match.group(3)} ({complete}/{total})")
            return f"{match.group(1)}{match.group(2)}{match.group(3)} ({complete}/{total})"
        new_text = pattern.sub(replace, text)
        if new_text != text and not dry:
            atomic_write(readme, new_text)
    return updated


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    table_updates = 0
    issues: list[str] = []
    for readme in sorted(root.rglob("README.md")):
        if any(part in {".git", "skill-ctf-writeup-sync"} for part in readme.relative_to(root).parts):
            continue
        create_others_event_table(readme, root, args.dry_run)
        _, total, found, changed = process(readme, root, args.dry_run)
        table_updates += int(changed)
        issues.extend(found)
    progress_updates = update_progress(root, args.dry_run)
    print(f"{'Would update' if args.dry_run else 'Updated'} {table_updates} README tables and {progress_updates} progress links.")
    if issues:
        print("Unresolved:")
        print("\n".join("- " + issue for issue in issues))


if __name__ == "__main__":
    main()
