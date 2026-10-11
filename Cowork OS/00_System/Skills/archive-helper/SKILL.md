---
name: archive-helper
description: Prepares a MEMORY.md -> ARCHIVE.md move as a ready-to-confirm plan (exact append text + exact lines to remove) without executing anything. Use when a project completes, the owner approves closing something out, a MEMORY.md needs the archive step of the 150-line procedure, or the owner says "archive this" / "close out X".
---

# Archive Helper

Last updated: 2026-09-28 (living document; Cowork OS Starter Kit v1.0)

## What this is

The archiving procedure from the memory-maintenance skill, made
deterministic. Archiving is the workspace's most
delicate routine edit — it removes text from a MEMORY.md — so this script
formats the entire move (verbatim block, `## [Workstation] Topic (archived
YYYY-MM-DD)` header, newest-first placement) and stops. **It never writes.**
A human/agent applies the two edits only after the owner confirms.

## When to run

- The owner confirms a project or verdict is closed (e.g. a finished project's final outcome, pending the owner's go-ahead).
- A MEMORY.md exceeds 150 lines and compression wasn't enough (memory-maintenance step 2).
- The dashboard shows a Dormant workstation that is actually done **[CONFIRM WITH OWNER]**.

## Procedure

1. List the archivable sections:

   ```
   python3 -B "00_System/Skills/archive-helper/scripts/prepare_archive.py" "<workspace root>" "<Workstation Name>"
   ```

   (`root` targets the root MEMORY.md; nested workstation names resolve too.)
2. Prepare the move for one section:

   ```
   python3 -B ... "<workspace root>" "<Workstation Name>" --section "<heading substring>"
   ```

3. **[CONFIRM WITH OWNER]** Show the owner the printed plan verbatim. Wait.
4. On confirmation, apply exactly the two edits: append block 1 to
   `ARCHIVE.md` directly below the marker line (newest first, above older
   entries); remove the listed lines from the source MEMORY.md.
5. Run the printed follow-ups: Current Status update, dashboard regen.

## What NOT to do

- Don't archive on inference — "looks done" isn't done; the owner's explicit confirmation gates step 4 every time.
- Don't summarize-and-delete: the block moves verbatim (memory-maintenance rule).
- Don't rewrite or reorder existing ARCHIVE.md entries — append-only, newest first.
- Don't use this for compression (that's an in-place MEMORY.md edit, not a move).

## Editing this skill

The header format and marker text live at the top of
`scripts/prepare_archive.py`; keep them in sync with the memory-maintenance
skill and root AGENTS.md if those change.
