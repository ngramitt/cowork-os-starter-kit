---
name: new-workstation
description: Scaffold a new Cowork OS workstation, nested parent or sub-workstation exactly per the template in 00_System/CONVENTIONS.md. Use whenever the owner asks to create a workstation or add an area, or when a task matches no Routing Map row and looks like the start of a recurring new area.
---

# New Workstation

Last updated: 2026-09-28 (living document; Cowork OS Starter Kit v1.0)

## What this is

The "Creating New Workstations" template from `00_System/CONVENTIONS.md`, made deterministic. The biggest cause of early mess in the original system was inconsistent scaffolds: empty Resources folders and missing or oddly named indexes. The script makes that impossible. Every workstation is born with `CLAUDE.md`, `MEMORY.md` and a `<Name> Resources/` folder carrying a starter `00_INDEX.md`.

## Procedure

1. **Confirm the name and placement in one short line:** top level, a nested parent, or an area under an existing parent. If the owner already gave a clear name for an obviously top-level area, just confirm as you go. Creating a workstation is a structural change; don't do it speculatively.
2. **Run the script.** It is create-only, and refuses if the folder exists.

   ```
   python3 -B "00_System/Skills/new-workstation/scripts/scaffold.py" "Name"
   python3 -B "00_System/Skills/new-workstation/scripts/scaffold.py" "Parent" --as-parent
   python3 -B "00_System/Skills/new-workstation/scripts/scaffold.py" "Area" --parent "Parent"
   ```

   Create a nested parent before its first area. A nested parent plus its first area is one area to the owner, even though it makes two folders.

   **Without Python:** create the same three files by hand, copying the templates in `00_System/CONVENTIONS.md` exactly, with today's date.
3. **Add the routing rows the script prints.** They're required: without them, sessions won't load the workstation, and the audit flags it.
   - **Top level:** one row in the root `AGENTS.md` Routing Map.
   - **Area under a parent:** a `Parent → Area` row in the root Routing Map, *and* a row in the parent's Sub-Routing Map.
   - **Nested parent:** no row of its own; its areas' rows route to it.

   Write each route condition in the owner's words, naming the specific things that should route there (people, projects, places, tools).
4. **Fill it in:** the Identity paragraph and a simple Workflow in `CLAUDE.md`, and the Current Status in `MEMORY.md` (state, next action, as-of date). If there are to-dos, create `<Name> Resources/Tracking/Tasks.md` in the format in `00_System/CONVENTIONS.md`, add it to that `00_INDEX.md`, and add a pointer line to the root `TASKS.md`.
5. **Record it:** add a line to today's dated changelog in `00_System/` (create `YYYY-MM-DD-Changelog.md` if there isn't one today, and add it to `00_System/00_INDEX.md`).
6. **Check:** regenerate the dashboard and run the audit with `--warn-only`, or do the by-hand checklist without Python.

As content arrives later, group it into typed subfolders under Resources. Every time you add a file, add it to that folder's `00_INDEX.md` and bump the index's `Last updated` date.

## Notes

- Sub-workstations get the one-line sub-workstation callout at the top of their `CLAUDE.md` automatically.
- The templates live inside `scripts/scaffold.py` and are copied into `00_System/CONVENTIONS.md`. If you change one, change the other in the same session.
