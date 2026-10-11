#!/usr/bin/env python3
"""Proves a restructure lost nothing. For each BACKUP=CURRENT pair, every
non-blank line that is in the backup but no longer in the current file must
exist, word for word, in some text file in the workspace (where it was moved).

Report-only. Exit 0 = nothing missing; exit 1 = lines to review.
Expected misses are lines you edited on purpose ("Last updated" stamps,
corrected facts, rewritten workflow lines). List them in the changelog.

Usage (from the workspace root; keep backups OUTSIDE the workspace):
  python3 -B 00_System/Skills/architecture-review/scripts/verify_moves.py \
      ~/bak/MEMORY.md=MEMORY.md "~/bak/Job__MEMORY.md=Job Search/MEMORY.md"
"""
import os, sys
from pathlib import Path

TEXT = {".md", ".txt", ".csv", ".json", ".py", ".html"}


def corpus(root):
    lines = set()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for f in filenames:
            p = Path(dirpath) / f
            if p.suffix.lower() in TEXT:
                try:
                    lines.update(p.read_text(errors="ignore").split("\n"))
                except OSError:
                    pass
    return lines


def main(pairs):
    root = Path.cwd()
    if not (root / "00_System").is_dir():
        sys.exit("Run from the Cowork OS root.")
    allc, missing_total, checked = corpus(root), 0, 0
    for pair in pairs:
        bak, _, cur = pair.partition("=")
        before = Path(os.path.expanduser(bak)).read_text().split("\n")
        now = set((root / cur).read_text().split("\n")) if (root / cur).exists() else set()
        removed = [l for l in before if l.strip() and l not in now]
        missing = [l for l in removed if l not in allc]
        checked += sum(1 for l in before if l.strip()); missing_total += len(missing)
        print(f"{cur}: {len(removed)} line(s) left this file, {len(removed) - len(missing)} found elsewhere, {len(missing)} not found")
        for l in missing:
            print(f"    MISSING: {l[:140]}")
    print(f"\n{checked} line(s) checked; {missing_total} not found verbatim anywhere.")
    return 1 if missing_total else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1:]))
