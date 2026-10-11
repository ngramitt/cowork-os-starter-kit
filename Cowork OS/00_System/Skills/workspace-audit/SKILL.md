---
name: workspace-audit
description: Deterministic health check for the Cowork OS workspace. Run at end of session whenever files were added/moved, before any structural reorganization, or when the owner asks "is the workspace clean?", "audit the workspace", or "end-of-session check". Zero-token — a Python script does all the checking; the agent only reads the report.
---

# Workspace Audit

Last updated: 2026-09-28 (living document; Cowork OS Starter Kit v1.0)

## What this is

The end-of-session check from `00_System/CONVENTIONS.md` ("File Placement & Folder
Structure", rule 7), made deterministic. Instead of an agent re-interpreting
the prose conventions each session — the drift vector described in
`00_System/DESIGN-NOTES.md`: a script checks
them mechanically and identically every time, on any model.

## When to run

- End of any session that added, moved, or renamed files (CONVENTIONS rule 7).
- End of any session that edited a MEMORY.md. Use `--warn-only`: WARN findings in full, INFO as a one-line count.
- Before and after any structural reorganization (pair with a changelog in `00_System/`).
- Whenever the owner asks for a workspace health check.
- The monthly structure audit scheduled task. Its prompt is `MONTHLY-AUDIT-PROMPT.md` next to this file; it only runs the script and reports.

## How to run

From the workspace root:

```
python3 -B "00_System/Skills/workspace-audit/scripts/audit.py" "<workspace root>"
```

Add `--warn-only` for the short end-of-session form. Dates in the report are the owner's local date (the timezone in `00_System/workspace-config.txt`), not the machine clock.

If run without an argument it finds the workspace root by walking up from its
own location. Requires only Python 3 stdlib. Exit 0 = clean, 1 = findings.

## What it checks

1. Every `MEMORY.md` under the 150-line cap (memory hygiene rule 2).
2. Workstation roots hold only `CLAUDE.md`, `MEMORY.md`, the Resources folder, and sub-workstations — no loose files.
3. Every Resources folder (and `00_Resources/`, `00_System/`) has a `00_INDEX.md`, its "Last updated" date isn't older than its newest file, and its direct children are mentioned in it.
4. At most one driver doc besides `00_INDEX.md` at a Resources root.
5. Cruft: `__pycache__/`, `.pyc`/`.pyo` (the only auto-removable class — and even these only get reported).
6. Backticked file references that no longer resolve (dangling paths after moves/renames) — in every `CLAUDE.md`, `MEMORY.md`, `00_INDEX.md`, **and every living reference doc** (any `.md` with a "Last updated:" line near the top). Excluded: AUTO-GENERATED files, date-prefixed artifacts (point-in-time snapshots), and `00_System/Skills/` (SKILL.mds cite pattern paths as examples). A reference also resolves when it names a file in the Skills library (a doc citing `scripts/score.py`) or, for `00_System` and `00_Resources` indexes, any file in the workspace; template placeholders (`YYYY-MM-DD-...`) and files inside `_archive/` or `_superseded/` folders are skipped.
7. **Size budgets.** MEMORY.md over 1,200 words (WARN), a Current Status section over 80 words (WARN), any MEMORY.md line over 60 words (INFO). The 150-line cap alone can be met with very long lines, which is how memory files grew to 5,000 words while passing.
8. Root `AGENTS.md` (the root rules file) over 11 KB (WARN) and any workstation `CLAUDE.md` over 10 KB (INFO): these load into sessions before any work.
9. `STATE.md` driver docs over 40 lines (INFO).
10. `TASKS.md`: more than 20 open items in Active (WARN), items over 25 words, and checked items still sitting in Active (INFO).
11. Collision names like `SKILL (1).md`: WARN when the un-suffixed original is missing (its references dangle), INFO when both copies exist. Cloud sync tools and browsers create these when a file is saved twice.
12. Heavy folders: `_`-prefixed or `build`/`cache`/`tmp`/`ocr` folders over 20 MB (INFO), as candidates to keep out of a cloud-synced folder.
13. **Routing.** Every workstation has a routing row: a row in the root Routing Map (`Parent → Area` for a sub-workstation), or a row in its parent's Sub-Routing Map or Sub-Areas table. Every such row points at a real workstation. Both are WARN. `scaffold.py` prints the row to add; this check catches a row that was never added, or one left behind by a rename.

## Without Python (the by-hand checklist)

If `python3` isn't available, do these five checks by reading the files, and say in your report that it was a by-hand check:

1. **Loose files:** each workstation root holds only `CLAUDE.md`, `MEMORY.md`, its `<Name> Resources/` folder and any sub-workstation folders.
2. **Indexes:** every Resources folder has a `00_INDEX.md` that mentions each of its direct children, and its `Last updated` date isn't older than the newest file you touched there.
3. **Status budgets:** each Current Status you edited is 80 words or fewer, and each `MEMORY.md` you edited is under about 1,200 words.
4. **Routing:** every workstation folder has a row in the root `AGENTS.md` Routing Map (`Parent → Area` for sub-workstations), every row points at a real folder, and each nested parent's Sub-Routing Map lists its areas.
5. **References:** file paths you wrote in backticks this session point at files that exist.

## How to act on the report

**The script never modifies anything, and neither should you without
confirmation.** For each finding:

- **WARN — stale index:** update that `00_INDEX.md` yourself (updating an index is part of the save step, not a destructive change) and bump its "Last updated" line.
- **WARN — loose files / missing Resources folder:** propose the exact moves to the owner and wait for their confirmation before executing (the owner's global rule). Remember rule 3: deliberate patterns (numbered handbooks, self-contained project folders with their own index, scaffolds like `_PROJECT-TEMPLATE/`) must NOT be forced apart — ask, don't assume.
- **INFO — unindexed items:** add them to the index, or confirm they're covered by a collective entry.
- **INFO — dangling references:** find where the file went (check the latest changelog in `00_System/`) and fix the reference.
- **INFO — cruft:** show the owner before deleting, even for regenerable artifacts.
- **Budget findings (checks 7 to 10):** never trim or delete to meet a budget. Move dated narrative verbatim into the workstation's `Progress Log/Progress-Log.md` (memory-maintenance skill), leave a pointer, and show the owner the plan first. Budgets warn; they never block.
- **Routing (check 13):** add the missing row (draft the route condition with the owner and show the owner the text first), or fix a row a rename left behind. Rewording existing rows risks misrouting, so change only what the finding names.
- **Collisions and heavy folders (checks 11 and 12):** report them. Renames use `mv -n` after the owner confirms; heavy folders are the owner's call.

**Known accepted findings** live in `accepted-findings.txt` (next to this
file): substring patterns for findings the owner has confirmed as deliberate; the
script suppresses matches automatically and reports only a count. Add a
pattern ONLY after the owner confirms, with a dated comment explaining why.
Built-in exemption: a Resources root holding only a numbered + indexed
sequence (3+ files like `01-...`, `02-...`) is treated as a deliberate
handbook (placement rule 3) and not flagged.

## Editing this skill

The check thresholds live at the top of `scripts/audit.py` (`MEMORY_LINE_CAP`,
the budget constants such as `MEMORY_WORD_BUDGET` and `STATUS_WORD_BUDGET`,
allowed root files, cruft lists). Run it with `python3 -B` so it leaves no
`__pycache__` behind. Per-workstation budget exceptions go in
`budget-overrides.txt` next to this file (one line each, dated reason,
only on the owner's word); the dashboard's ⚠ flag reads the same file. If a root AGENTS.md convention changes,
update the script in the same session and note it here.
