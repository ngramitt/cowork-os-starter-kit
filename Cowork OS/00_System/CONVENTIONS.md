# CONVENTIONS: Cowork OS

Last updated: 2026-09-28 (living document; Cowork OS Starter Kit v1.0)

The full workspace conventions. **They carry the same authority as the root `AGENTS.md`**, which keeps a short stub under each of these headings and points here. The root file holds the Memory System, File naming, Preferences, Rules, Routing Map and References.

## Memory hygiene rules (full)

1. Keep each memory entry to two sentences max.
2. Keep every `MEMORY.md` (root and workstation) under 150 lines and 1,200 words. If one grows past that, move dated narrative into the workstation's Progress Log first (verbatim, leaving a pointer), then archive completed items.
3. Current-state content (active work, contact info, working conventions) stays in `MEMORY.md` regardless of age.
4. When a project completes or an entry becomes outdated, propose moving it from `MEMORY.md` to the root `ARCHIVE.md`, tagged with its workstation name, and move it once I confirm.
5. `ARCHIVE.md` is reference-only: never read at session start, only pulled up when I ask about something historical.

## File Placement & Folder Structure

This section governs *where a file lives* (the naming rules in the root file govern what it's called). It exists because reference docs tend to land at the root of a Resources folder one harmless-looking save at a time, until there's a large flat pile no naming rule catches. Placement is a deliberate step, not a default.

1. **Everything for a workstation lives inside its `[Workstation] Resources/` folder.** A workstation root holds only `CLAUDE.md`, `MEMORY.md` and that Resources folder (plus, for a nested parent, its sub-workstation folders). Never leave loose deliverables, downloads or drafts at the workstation root. Move them into Resources the moment they land.
2. **Inside Resources, group reference docs into typed subfolders** named by purpose, e.g. `Strategy and Analysis/`, `Correspondence/`, `Evidence/`, `Knowledge Base/`, `Briefs/`, `Tracking/`, `Progress Log/`, `Handoffs/`. Only two things may sit at the Resources *root*: the `00_INDEX.md` catalogue, and the workstation's single source-of-truth driver doc (a checklist, tracker, or living plan). When a second doc of a type appears at the root, create or reuse a subfolder.
3. **Don't over-fold either.** Deliberate clean patterns are fine as they are: a small numbered, indexed sequence (a `01` to `09` handbook), a self-contained project folder with its own index, or a scaffold template. The principle is "no orphan files at a root and no mixed-purpose piles," not "one file per folder."
4. **Every Resources folder (and every self-contained project folder) carries a `00_INDEX.md`** with that exact filename. It maps the contents: path, purpose, and whether each doc is living or immutable. Updating the index is part of the save step, not a later cleanup.
5. **When you move or rename a file, rewrite every reference to it** in the workstation's `CLAUDE.md`, `MEMORY.md`, `00_INDEX.md` and any doc-to-doc links, then confirm nothing dangles. Show me the moves before executing and wait for my OK.
6. **Keep workstations free of system cruft, but never auto-delete anything.** Only unambiguous machine-regenerable build artifacts (`__pycache__/`, `.pyc`, `.pyo`) are even candidates for removal, and even these get shown to me first. Anything that merely *looks* disposable is presumed deliberate until I say otherwise. That especially includes `_`-prefixed files and folders (often the source-of-truth originals), anything named `scratch`, `draft`, `notes`, `tmp` or `test`, intermediate data files, and cloud-sync staging files like `.tmp.drive*`. When unsure, flag it; don't delete it. Leave `.DS_Store` files alone; macOS manages them.
7. **End-of-session check:** if a session added or moved files, verify before wrapping up that nothing is loose at a workstation root or Resources root and that the relevant `00_INDEX.md` reflects reality. If a session edited any `MEMORY.md`, run `python3 -B 00_System/Skills/workspace-audit/scripts/audit.py --warn-only` before wrapping up.

## The `00_System/` Folder

`00_System/` holds **records about the workspace itself**, not domain content: these conventions, `DESIGN-NOTES.md`, `ROADMAP.md`, `GUIDE.md`, `workspace-config.txt`, the `Skills/` library, and dated changelogs.

- **Write here when** you do a structural reorganization, a cross-workstation cleanup, or anything that changes *where files live*. Record a dated changelog listing every old → new path, plus the reasoning if a pattern caused it.
- **Read here when** a path that used to work suddenly doesn't (check the latest changelog), or when you need to understand why the structure is the way it is before changing it.
- **Never put** workstation deliverables here, and never route a domain task here. It has no `CLAUDE.md` or `MEMORY.md`; its `00_INDEX.md` catalogues what's inside.

## Skills (`00_System/Skills/`)

Reusable procedures and deterministic scripts that standardize this workspace's recurring operations, so any AI tool or model runs them the same way. Before improvising one of these operations, read the matching `SKILL.md` and follow it. Scripts are Python 3 standard library only, and either report-only or create-only; nothing there deletes or overwrites. `00_System/Skills/00_INDEX.md` is the full catalogue.

| Skill | Use when... |
|---|---|
| `first-run-setup` | The root `AGENTS.md` says "Not set up yet," or I say "re-run setup." |
| `workspace-audit` | Ending a session that added or moved files or edited a `MEMORY.md`; before or after any reorganization; I ask for a health check. |
| `new-workstation` | Creating any workstation or sub-workstation. Never scaffold by hand when Python is available. |
| `memory-maintenance` | I say "remember this"; a `MEMORY.md` gets long; something finished and needs archiving. |
| `work-dashboard` | I ask what's active or what's on my plate; any session that changed a Current Status. |
| `project-lifecycle` | Starting a project, ending a working session on one, a deliverable ships, or I say something is done. |
| `session-handoff` | Ending a session with work mid-flight, or packaging work for a fresh session, model or tool. |
| `archive-helper` | Something is confirmed done and its memory should move to `ARCHIVE.md`. |
| `architecture-review` | I ask to optimize, review or rethink the whole workspace, or about once a year. |

New skills: copy the template in `00_System/Skills/SKILL-TEMPLATE.md` and follow its authoring rules.

## Creating New Workstations

When I ask for a new workstation, confirm the name and whether it sits at the top level, is a nested parent, or is an area under a parent. Then run the new-workstation skill (`00_System/Skills/new-workstation/SKILL.md`). With Python, its script creates the files; without Python, create them by hand from the templates below, word for word, with today's date.

After creating it:
- Add the routing rows. A top-level workstation gets one row in the root `AGENTS.md` Routing Map. An area gets a `Parent → Area` row there and a row in its parent's Sub-Routing Map. A nested parent needs no row of its own. The audit flags a workstation without a row.
- Add a line to today's dated changelog in `00_System/`.

**`<Name>/CLAUDE.md`** (the workstation's rules file, whichever AI tool reads it):

```
# CLAUDE.md: <Name>

## Identity

_One paragraph: who you are in this workstation, what routes here, and what doesn't. Draft it with the owner._

## Resources

| Resource | Read when... |
|---|---|
| `<Name> Resources/00_INDEX.md` | Always the entry point: it maps every doc in this workstation. |

## Workflow

_Numbered steps for this workstation's main job. Start simple; refine over time._

1. Check MEMORY.md Current Status for where things stand.
2. Do the next action; update the driver doc or tracker as part of the work.
3. Update Current Status (80 words or fewer). Session narrative goes to the Progress Log in Resources (Progress Log/Progress-Log.md), and decisions go to the Decision Log next to it.

## Standing Rules

_"Always" and "never" rules for this area, added as they come up._

## Editorial Rules

Follow my voice principles in 00_Resources (voice-principles.md).
```

A sub-workstation's `CLAUDE.md` adds this callout right under its title: `> **This is a sub-workstation** under the **<Parent>** parent. ...`. A nested parent's `CLAUDE.md` has Identity, a **Sub-Routing Map** table (`| Area | Route here when I... |`), Resources and Editorial Rules instead of Workflow and Standing Rules.

**`<Name>/MEMORY.md`:**

```
# <Name> Memory

## Current Status

_State, blocker, next action and as-of date: 80 words or fewer. Update every working session._

- **State (as of YYYY-MM-DD):** ...
- **Blocker:** ... (leave out if none)
- **Next action:** ...

## Contacts

_People relevant to this area._

## Key Decisions

_One line per decision; the full reasoning goes in the Decision Log._
```

**`<Name>/<Name> Resources/00_INDEX.md`:**

```
# 00_INDEX: <Name> Resources

_Last updated: YYYY-MM-DD. This index maps everything in `<Name> Resources/`. Updating it (and this date) is part of every save or move, not a later cleanup. Only this file and one driver doc may sit at the Resources root; group reference docs into typed subfolders like `Tracking/`, `Progress Log/`, `Correspondence/`._

| Doc | Type | What it's for |
|---|---|---|

_Legend: 🟢 living (update in place) · 📄 immutable (dated artifact)._
```

## Task lists

Each workstation with to-dos keeps `<Name> Resources/Tracking/Tasks.md`. Add it to that Resources `00_INDEX.md` when you create it. The format:

```
# Tasks: <Name>

Last updated: YYYY-MM-DD. One task per line. A task marked done moves to Done in the same session.

## Active

- [ ] **Short task name:** one line of detail or a pointer

## Waiting On

## Someday

## Done

- [x] Finished task (YYYY-MM-DD)
```

The dashboard counts the `- [ ]` lines under `## Active` as open tasks. The root `TASKS.md` holds one pointer line per workstation under Active, written as a plain bullet so it isn't counted as a task: `- **<Name>:** <path to its Tasks.md>`.

## Nested Parent Workstations & Sub-Workstations

Some domains are too broad for one workstation and split into areas, e.g. **Creative Projects** → **Photography**, with more areas like Writing or Music to come.

- **A nested parent** (e.g. Creative Projects) routes to its areas rather than doing the hands-on work itself. Its own Resources folder holds only material that spans all its areas. Its `CLAUDE.md` has a **Sub-Routing Map** table (Area | Route here when...).
- **A sub-workstation** (e.g. Photography) is a **full workstation**, with its own `CLAUDE.md`, `MEMORY.md` and `[Area] Resources/`. It lives at the **parent's root, as a sibling of the parent's Resources folder, never inside it**. A Resources folder holds reference docs, not workstations.
- **Marking:** every sub-workstation's `CLAUDE.md` opens with a one-line callout declaring that it is a sub-workstation and naming its parent. The scaffold script writes it.
- **Routing:** the root Routing Map uses the `Parent → Area` form (e.g. "Creative Projects → Photography"), and the parent's Sub-Routing Map lists the area by name. The most specific area's rules win within its domain.
