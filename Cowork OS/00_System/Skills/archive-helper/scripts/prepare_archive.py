#!/usr/bin/env python3
"""
Archive helper — prepares (never executes) a MEMORY.md -> ARCHIVE.md move.

REPORT-ONLY: prints the exact text to append to ARCHIVE.md and the exact
lines to remove from the source MEMORY.md, formatted per the
memory-maintenance skill. A human/agent applies the change only after
the owner's confirmation. This script writes nothing.

Usage:
    # list the archivable sections of a MEMORY.md
    python3 prepare_archive.py <workspace_root> <workstation-or-memory-path>

    # prepare the move for one section (heading matched by substring, case-insensitive)
    python3 prepare_archive.py <workspace_root> <workstation-or-memory-path> --section "Current Status"

<workstation-or-memory-path> may be a workstation folder name (e.g.
"Job Search"), a path to a MEMORY.md, or "root" for the root
MEMORY.md.

Exit code: 0 = ok, 2 = usage/resolution error.
"""

import sys
from datetime import datetime
from zoneinfo import ZoneInfo

from pathlib import Path


def _load_local_tz():
    """The owner's timezone from 00_System/workspace-config.txt (written during
    first-run setup). Falls back to this machine's local timezone, so dates
    match the owner's calendar rather than a UTC server clock."""
    here = Path(__file__).resolve()
    for cand in here.parents:
        cfg = cand / "00_System" / "workspace-config.txt"
        if cfg.is_file():
            for line in cfg.read_text(encoding="utf-8").splitlines():
                key, _, val = line.partition("=")
                if key.strip().lower() == "timezone" and val.strip():
                    try:
                        return ZoneInfo(val.strip())
                    except Exception:
                        break
            break
    return datetime.now().astimezone().tzinfo


LOCAL_TZ = _load_local_tz()
from pathlib import Path

MARKER = "<!-- Archived entries go below this line"


def resolve_memory(root: Path, token: str):
    if token.lower() == "root":
        return root / "MEMORY.md", None
    p = Path(token)
    if p.name == "MEMORY.md":
        cand = p if p.is_absolute() else root / p
        if cand.is_file():
            ws = cand.parent.name if cand.parent != root else None
            return cand, ws
    cand = root / token / "MEMORY.md"
    if cand.is_file():
        return cand, token
    # nested workstation search (e.g. "Photography")
    for m in root.rglob("MEMORY.md"):
        if m.parent.name.lower() == token.lower():
            return m, m.parent.name
    return None, None


def sections(lines):
    """Yield (title, level, start, end) for every #-heading section."""
    heads = [(i, line) for i, line in enumerate(lines)
             if line.lstrip().startswith("#")]
    out = []
    for n, (i, line) in enumerate(heads):
        level = len(line) - len(line.lstrip("#").join([""]))  # placeholder
        level = len(line.lstrip()) - len(line.lstrip().lstrip("#"))
        title = line.lstrip().lstrip("#").strip()
        end = len(lines)
        for j, jline in heads[n + 1:]:
            jlevel = len(jline.lstrip()) - len(jline.lstrip().lstrip("#"))
            if jlevel <= level:
                end = j
                break
        out.append((title, level, i, end))
    return out


def main():
    args = [a for a in sys.argv[1:]]
    if len(args) < 2:
        print(__doc__)
        return 2
    root = Path(args[0]).resolve()
    if not (root / "CLAUDE.md").is_file() or not (root / "00_System").is_dir():
        print(f"ERROR: {root} doesn't look like the workspace root "
              f"(needs CLAUDE.md + 00_System/).")
        return 2
    section_pat = None
    if "--section" in args:
        k = args.index("--section")
        if k + 1 >= len(args):
            print("ERROR: --section needs a value.")
            return 2
        section_pat = args[k + 1]
        del args[k:k + 2]
    mem, ws = resolve_memory(root, args[1])
    if mem is None:
        print(f"ERROR: couldn't resolve '{args[1]}' to a MEMORY.md under {root}.")
        return 2

    lines = mem.read_text(encoding="utf-8", errors="replace").splitlines()
    secs = [s for s in sections(lines) if s[1] >= 2]  # skip the H1 title

    if section_pat is None:
        print(f"# Archivable sections in {mem.relative_to(root)}")
        print("(pick one and re-run with --section \"<substring>\")\n")
        for title, level, i, end in secs:
            print(f"- [{end - i} lines, starts line {i + 1}] {title}")
        if not secs:
            print("(no ##+ sections found — this MEMORY.md may use flat bullets;")
            print(" prepare the move by hand per the memory-maintenance skill)")
        return 0

    matches = [s for s in secs if section_pat.lower() in s[0].lower()]
    if len(matches) != 1:
        print(f"ERROR: '{section_pat}' matched {len(matches)} section(s):")
        for title, *_ in matches:
            print(f"  - {title}")
        print("Narrow the substring so exactly one matches.")
        return 2

    title, level, i, end = matches[0]
    block = lines[i:end]
    # trim trailing blank lines from the block
    while block and not block[-1].strip():
        block.pop()
    today = datetime.now(LOCAL_TZ).date().isoformat()
    tag = f"[{ws}] " if ws else ""
    header = f"## {tag}{title} (archived {today})"
    body = [l for l in block[1:]]  # drop the original heading

    print("=" * 70)
    print("ARCHIVE PREPARATION — REPORT ONLY. Nothing has been modified.")
    print("Per the owner's rules: show the owner this plan and WAIT for confirmation")
    print("before applying either edit below.")
    print("=" * 70)
    print(f"\nSource: {mem.relative_to(root)}, lines {i + 1}-{i + len(block)} "
          f"({len(block)} lines)")
    print(f"Target: ARCHIVE.md (append directly below the marker line, "
          f"newest first)\n")
    print("--- 1) TEXT TO APPEND to ARCHIVE.md (verbatim, below the marker) ---\n")
    print(header)
    print("\n".join(body).strip("\n"))
    print("\n--- 2) LINES TO REMOVE from the source MEMORY.md ---\n")
    for n, l in enumerate(block, start=i + 1):
        print(f"{n:4d} | {l}")
    print("\n--- 3) FOLLOW-UPS after the owner confirms and the edits are applied ---\n")
    print("- If a whole project completed: set the workstation MEMORY.md")
    print("  Current Status to 'Complete — ... Next action: none.'")
    print("- Regenerate the dashboard (work-dashboard skill).")
    print("- ARCHIVE.md is append-only, newest first — never rewrite history.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
