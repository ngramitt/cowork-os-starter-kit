#!/usr/bin/env python3
"""
Cowork OS workstation scaffolder.

Creates a new workstation, nested parent or sub-workstation exactly per the
template in 00_System/CONVENTIONS.md ("Creating New Workstations" / "Nested
Parent Workstations & Sub-Workstations"). Create-only: refuses to run if the
target folder already exists, and never edits an existing file.

Usage:
    python3 -B scaffold.py "Name" [--as-parent] [--parent "Parent[/Area]"] [--root WORKSPACE_ROOT]

Examples:
    python3 -B scaffold.py "Home"                                   # a workstation
    python3 -B scaffold.py "Creative Projects" --as-parent          # a nested parent
    python3 -B scaffold.py "Photography" --parent "Creative Projects"   # an area under it

Create a nested parent before its first area. After running, the script
prints the created paths and the exact routing rows to add; adding them is
the agent's follow-up step (the audit flags a workstation without a row).
"""

import argparse
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

CLAUDE_TEMPLATE = """# CLAUDE.md: {name}
{subcallout}
## Identity

_One paragraph: who you are in this workstation, what routes here, and what doesn't. Draft it with the owner._

## Resources

| Resource | Read when... |
|---|---|
| `{name} Resources/00_INDEX.md` | Always the entry point: it maps every doc in this workstation. |

## Workflow

_Numbered steps for this workstation's main job. Start simple; refine over time._

1. Check MEMORY.md Current Status for where things stand.
2. Do the next action; update the driver doc or tracker as part of the work.
3. Update Current Status (80 words or fewer). Session narrative goes to the Progress Log in Resources (Progress Log/Progress-Log.md), and decisions go to the Decision Log next to it.

## Standing Rules

_"Always" and "never" rules for this area, added as they come up._

## Editorial Rules

Follow my voice principles in 00_Resources (voice-principles.md).
"""

PARENT_TEMPLATE = """# CLAUDE.md: {name}

## Identity

This is the {name} nested parent. It routes to its areas and doesn't do the hands-on work itself. When a task clearly belongs to an area, enter that area's folder and read its CLAUDE.md and MEMORY.md before doing any work. Its own Resources folder holds only material that spans all its areas.

## Sub-Routing Map

_Check this table to decide which area applies. Add a row each time an area is created. Area rules layer on top of this file and the root files; the most specific area wins within its domain._

| Area | Route here when I... |
|---|---|

## Resources

| Resource | Read when... |
|---|---|
| `{name} Resources/00_INDEX.md` | Cross-area material only. |

## Editorial Rules

Follow my voice principles in 00_Resources (voice-principles.md).
"""

SUB_CALLOUT = """
> **This is a sub-workstation** under the **{parent}** parent. It is a full workstation with its own `CLAUDE.md`, `MEMORY.md` and `{name} Resources/`, and it sits at the parent's root beside the parent's Resources folder, never inside it. See `00_System/CONVENTIONS.md` → "Nested Parent Workstations & Sub-Workstations".
"""

MEMORY_TEMPLATE = """# {name} Memory

## Current Status

_State, blocker, next action and as-of date: 80 words or fewer. Update every working session._

- **State (as of {today}):** new workstation.
- **Next action:** {next_action}

## Contacts

_People relevant to this area._

## Key Decisions

_One line per decision; the full reasoning goes in the Decision Log._
"""

INDEX_TEMPLATE = """# 00_INDEX: {name} Resources

_Last updated: {today}. This index maps everything in `{name} Resources/`. Updating it (and this date) is part of every save or move, not a later cleanup. Only this file and one driver doc may sit at the Resources root; group reference docs into typed subfolders like `Tracking/`, `Progress Log/`, `Correspondence/`._

| Doc | Type | What it's for |
|---|---|---|

_Legend: 🟢 living (update in place) · 📄 immutable (dated artifact)._
"""


def find_root(start: Path):
    for cand in [start.resolve(), *start.resolve().parents]:
        if ((cand / "AGENTS.md").is_file() or (cand / "CLAUDE.md").is_file()) \
                and (cand / "00_System").is_dir():
            return cand
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name", help="New workstation name (folder name)")
    ap.add_argument("--parent", default=None,
                    help="Parent workstation path relative to root, e.g. "
                         "'Creative Projects' or 'Creative Projects/Photography'")
    ap.add_argument("--as-parent", action="store_true",
                    help="Create a nested parent (routes to areas; has a Sub-Routing Map)")
    ap.add_argument("--root", default=None, help="Workspace root path")
    args = ap.parse_args()

    root = Path(args.root).resolve() if args.root else find_root(Path(__file__).parent)
    if not root:
        print("ERROR: couldn't locate the workspace root; pass --root.")
        return 2

    base = root / args.parent if args.parent else root
    if args.parent and not (base / "CLAUDE.md").is_file():
        print(f"ERROR: parent '{args.parent}' is not a workstation yet (no "
              f"CLAUDE.md at {base}). Create it first: python3 -B "
              f"00_System/Skills/new-workstation/scripts/scaffold.py "
              f"\"{args.parent}\" --as-parent")
        return 2

    ws = base / args.name
    if ws.exists():
        print(f"ERROR: {ws} already exists. Refusing to touch it "
              f"(this script never overwrites).")
        return 2

    today = datetime.now(LOCAL_TZ).date().isoformat()
    res = ws / f"{args.name} Resources"
    res.mkdir(parents=True)

    if args.as_parent:
        claude = PARENT_TEMPLATE.format(name=args.name)
        next_action = "none at this level; work happens in its areas."
    else:
        subcallout = (SUB_CALLOUT.format(name=args.name, parent=args.parent)
                      if args.parent else "")
        claude = CLAUDE_TEMPLATE.format(name=args.name, subcallout=subcallout)
        next_action = "draft this workstation's Identity with the owner."
    (ws / "CLAUDE.md").write_text(claude, encoding="utf-8")
    (ws / "MEMORY.md").write_text(
        MEMORY_TEMPLATE.format(name=args.name, today=today, next_action=next_action),
        encoding="utf-8")
    (res / "00_INDEX.md").write_text(
        INDEX_TEMPLATE.format(name=args.name, today=today), encoding="utf-8")

    print("Created:")
    for p in (ws / "CLAUDE.md", ws / "MEMORY.md", res / "00_INDEX.md"):
        print(f"  {p.relative_to(root)}")
    print()
    if args.as_parent:
        print("FOLLOW-UP: a nested parent needs no Routing Map row of its own.")
        print("Its areas' 'Parent → Area' rows route to it. Create its first")
        print(f"area next: scaffold.py \"<Area>\" --parent \"{args.name}\"")
    elif args.parent:
        parent_md = (base / "CLAUDE.md").read_text(encoding="utf-8", errors="replace")
        label = " → ".join(args.parent.split("/") + [args.name])
        print("FOLLOW-UP (required), two rows:")
        print("1. In the root AGENTS.md Routing Map:")
        print(f"   | {label} | ...am working on ...(the owner's words) |")
        print(f"2. In the Sub-Routing Map of '{args.parent}/CLAUDE.md':")
        print(f"   | {args.name} | ...am working on ...(the owner's words) |")
        if "## Sub-Routing Map" not in parent_md and "## Sub-Areas" not in parent_md:
            print(f"   ('{args.parent}/CLAUDE.md' has no Sub-Routing Map yet: add a")
            print("   '## Sub-Routing Map' section with an 'Area | Route here when I...'")
            print("   table, as in 00_System/CONVENTIONS.md.)")
    else:
        print("FOLLOW-UP (required): add a row to the root AGENTS.md Routing Map:")
        print(f"  | {args.name} | ...am working on ...(the owner's words) |")
    print("\nThen: write the Identity (and Workflow) in the owner's words, set the")
    print("Current Status, add a line to today's dated changelog in 00_System/, and")
    print("run the audit. When you add files to a Resources folder later, add them")
    print("to its 00_INDEX.md and bump its 'Last updated' date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
