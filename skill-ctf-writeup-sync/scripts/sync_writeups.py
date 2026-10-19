#!/usr/bin/env python3
"""Synchronize challenge README status cells using exact, auditable mappings."""
from __future__ import annotations

import argparse
import csv
import html
import os
import re
import tempfile
import unicodedata
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

NAME_HEADERS = {"challenge", "challengename", "name", "exercise", "task", "problem", "bài"}
STATUS_HEADERS = {"writeup", "solution", "writeupstatus"}
ID_HEADERS = {"id", "#", "no", "number", "challengeid"}
PLACEHOLDERS = {"todo", "tbd", "chưa có write-up", "coming soon", "write-up coming soon"}


def norm(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(c for c in value if not unicodedata.combining(c)).casefold()
    return "".join(c for c in value if c.isalnum())


def read_text(path: Path) -> str:
    """Read UTF-8 without newline translation so edited Markdown keeps its EOLs."""
    with path.open("r", encoding="utf-8", newline="") as stream:
        return stream.read()


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
    value = line.rstrip("\r\n").rstrip(" \t")
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
    value = re.sub(r"<[^>]*>", "", cell).strip().strip("`*_").lstrip("\ufeff").casefold()
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


def alias_candidates(label: str, ident: str, readme: Path, base: Path, root: Path) -> list[Path]:
    """Read explicit, reviewed aliases from challenge-aliases.csv at repository root."""
    manifest = root / "challenge-aliases.csv"
    if not manifest.is_file():
        return []
    result = []
    with manifest.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {"readme", "challenge_id", "challenge", "directory"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError("challenge-aliases.csv requires columns: readme, challenge_id, challenge, directory")
        for row in reader:
            if row.get("readme", "").replace("\\", "/") != readme.relative_to(root).as_posix():
                continue
            row_id = row.get("challenge_id", "").strip()
            row_name = row.get("challenge", "").strip()
            if (row_id and row_id != ident) or (not row_id and norm(row_name) != norm(label)):
                continue
            relative = row.get("directory", "").strip()
            if not relative:
                continue
            target = (root / relative).resolve()
            try:
                target.relative_to(base.resolve())
            except ValueError:
                continue
            if target.is_dir() and (target / "write-up.md").is_file():
                result.append(target)
    return list(dict.fromkeys(result))


def map_candidate(label: str, cell: str, ident: str, readme: Path, base: Path, root: Path) -> tuple[Path | None, list[Path], str]:
    candidates = candidate_dirs(base, root)
    exact = [path for path in candidates if norm(path.name) == norm(label)]
    if len(exact) == 1:
        return exact[0], exact, "exact name"
    # Only the final URL path segment may provide the fallback match.
    url = re.search(r"\]\((?:<)?(https?://[^)>]+)", cell)
    if url:
        segment = unquote(urlsplit(url.group(1)).path.rstrip("/").split("/")[-1])
        matched = [path for path in candidates if norm(path.name) == norm(segment)]
        if len(matched) == 1:
            return matched[0], matched, "URL segment"
        if matched:
            exact = matched
    aliases = alias_candidates(label, ident, readme, base, root)
    if len(aliases) == 1:
        return aliases[0], aliases, "approved alias"
    if aliases:
        return None, aliases, "ambiguous alias"
    if len(exact) > 1:
        return None, exact, "ambiguous exact name"
    return None, [], "no exact match"


def replace_cell(line: str, cells: list[str]) -> str:
    """Replace one table cell while preserving outer pipes and line ending."""
    ending = "\r\n" if line.endswith("\r\n") else "\n" if line.endswith("\n") else ""
    raw = line[:-len(ending)] if ending else line
    leading = raw.startswith("|")
    trailing = raw.rstrip(" \t").endswith("|")
    return ("|" if leading else "") + "|".join(cells) + ("|" if trailing else "") + ending


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
    lines = read_text(readme).splitlines()
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
        if len(matches) > 1:
            return None
        if matches:
            courses.append((course, matches[0]))
    if len(courses) != 1:
        return None
    course, _ = courses[0]
    title = next((line.lstrip("# ").strip() for line in read_text(course).splitlines() if line.startswith("#")), course.parent.name)
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
    matches = [cell for name, cell in table_rows(target) if norm(name) == norm(label)]
    if len(matches) != 1:
        return False
    dest, linked = internal_writeup_link(matches[0], target.parent, root)
    if linked and dest:
        try:
            return meaningful(dest)
        except (OSError, UnicodeError):
            return False
    return status_is_external(matches[0])


def event_challenge_folders(parent: Path, root: Path) -> list[Path]:
    """Find challenge leaves for one event without crossing nested README indexes."""
    folders = set()
    for marker in ("write-up.md", "solve.py"):
        for path in parent.rglob(marker):
            if any(part in {".git", "skill-ctf-writeup-sync"} for part in path.relative_to(root).parts):
                continue
            folder = path.parent
            parts = folder.relative_to(parent).parts
            if (folder / "README.md").is_file() and folder != parent:
                continue
            if any((parent.joinpath(*parts[:index]) / "README.md").is_file()
                   for index in range(1, len(parts))):
                continue
            folders.add(folder)
    return sorted(folders)


def event_table_rows(folders: list[Path], readme_dir: Path) -> list[str]:
    grouped = all(len(folder.relative_to(readme_dir).parts) > 1 for folder in folders)
    groups: dict[str | None, list[Path]] = {}
    for folder in folders:
        relative = folder.relative_to(readme_dir).parts
        category = relative[0] if grouped else None
        groups.setdefault(category, []).append(folder)

    rows = []
    for category, challenges in groups.items():
        if category is not None:
            rows.extend([f"## {category}", ""])
        rows.extend(["| Challenge | Write-up |", "| --- | --- |"])
        for folder in challenges:
            writeup = folder / "write-up.md"
            if writeup.is_file() and meaningful(writeup):
                status = f"[Đọc write-up]({relative_link(writeup, readme_dir)})"
            else:
                status = "Chưa có write-up"
            rows.append(f"| {folder.name} | {status} |")
        rows.append("")
    if rows and rows[-1] == "":
        rows.pop()
    return rows


def create_missing_event_readmes(root: Path, dry: bool) -> int:
    """Create an event index when challenge folders exist but README.md does not."""
    events = root / "Others-Events"
    created = 0
    for year in sorted(path for path in events.iterdir() if path.is_dir()):
        for event in sorted(path for path in year.iterdir() if path.is_dir()):
            readme = event / "README.md"
            if readme.exists():
                continue
            folders = event_challenge_folders(event, root)
            if not folders:
                continue
            title = event.name.replace("_", " ")
            rows = [f"# {title}", "", *event_table_rows(folders, event)]
            if not dry:
                atomic_write(readme, "\n".join(rows) + "\n")
            created += 1
    return created


def create_others_event_table(readme: Path, root: Path, dry: bool) -> bool:
    """Create the required table for an event README that has challenge folders."""
    if "Others-Events" not in readme.relative_to(root).parts:
        return False
    if table_rows(readme):
        return False
    text = read_text(readme)
    for match in re.finditer(r"\[[^]]*\]\((?:<([^>]+)>|([^\s)]*))\)", text):
        target = unquote(match.group(1) or match.group(2))
        if urlsplit(target).scheme or urlsplit(target).netloc:
            continue
        child = (readme.parent / urlsplit(target).path).resolve()
        try:
            child.relative_to(readme.parent.resolve())
        except ValueError:
            continue
        if child != readme.resolve() and child.is_file() and child.name.casefold() == "readme.md":
            return False
    folders = event_challenge_folders(readme.parent, root)
    if not folders:
        return False
    rows = ["", *event_table_rows(folders, readme.parent)]
    if not dry:
        original = read_text(readme)
        newline = "\r\n" if "\r\n" in original else "\n"
        atomic_write(readme, original.rstrip("\r\n") + newline + newline.join(rows) + newline)
    return True


def process(readme: Path, root: Path, dry: bool) -> tuple[int, int, list[str], bool]:
    text = read_text(readme)
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
            if status.strip().casefold() in {"chưa có write-up", "todo", "tbd"}:
                linked_course = course_status(label, readme, root)
                if linked_course:
                    status = linked_course
            if status.lstrip().startswith("Đang nằm ở course"):
                if course_complete(status, label, readme, root):
                    done += 1
                desired = status
                if cells[status_col] != desired:
                    cells[status_col] = desired
                    lines[j] = replace_cell(lines[j], cells)
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
                dest, ambiguous, evidence = map_candidate(label, cells[name_col], ident, readme, readme.parent, root)
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
                lines[j] = replace_cell(lines[j], cells)
                changed = True
            j += 1
        i = j if j > i + 1 else i + 1
    if changed and not dry:
        atomic_write(readme, "".join(lines))
    return done, total, issues, changed


def row_completion(readme: Path, root: Path) -> tuple[int, int]:
    """Count completed rows from the current README contents."""
    lines = read_text(readme).splitlines()
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
        text = read_text(readme)
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
    created_event_readmes = create_missing_event_readmes(root, args.dry_run)
    changed_readmes = 0
    created_event_tables = 0
    issues: list[str] = []
    for readme in sorted(root.rglob("README.md")):
        if any(part in {".git", "skill-ctf-writeup-sync"} for part in readme.relative_to(root).parts):
            continue
        created_event_tables += int(create_others_event_table(readme, root, args.dry_run))
        _, total, found, changed = process(readme, root, args.dry_run)
        changed_readmes += int(changed)
        issues.extend(found)
    progress_updates = update_progress(root, args.dry_run)
    verb = "Would update" if args.dry_run else "Updated"
    event_verb = "would create" if args.dry_run else "created"
    print(f"{verb} {changed_readmes} README files, {event_verb} {created_event_readmes} event READMEs and {created_event_tables} event tables, and refresh {progress_updates} progress links.")
    if issues:
        print("Unresolved:")
        print("\n".join("- " + issue for issue in issues))


if __name__ == "__main__":
    main()
