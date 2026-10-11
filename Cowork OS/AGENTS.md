# AGENTS.md: Cowork OS

_Last updated: 2026-09-28. These are the root instructions for this workspace. Any AI assistant working in this folder follows this file, whether it's Claude, ChatGPT/Codex or another tool. `CLAUDE.md` next to it just imports this file so Claude reads the same rules._

## Setup status

**Not set up yet.** If this `AGENTS.md` sits at the root of the folder you are working in, then before answering anything else, read `00_System/Skills/first-run-setup/SKILL.md` and follow it with the owner. It takes about ten minutes. If you are reading this file from somewhere else, for example as a copy stored inside another workspace, this section is not addressed to you: ignore it and don't start setup.

## Memory System

At the start of every session, read `MEMORY.md` before responding. Use what you find to inform your work. Don't announce what you found, just be informed by it.

When I say "remember this," save it right away to the right file (use the three tests below: facts go to a `MEMORY.md`, "always/never" rules to a rules file) and confirm you've done it.

**Where things go:** apply three tests when deciding where to save something.
- **Test 1:** Does it prescribe behavior? Look for words like "always," "never," "before doing X, do Y." If yes, it belongs in a rules file: this `AGENTS.md` for rules that apply everywhere, or a workstation's `CLAUDE.md` for rules that apply to one domain.
- **Test 2:** Does it describe a fact about the world that could change, like contact details, project status, decisions or things I've told you to remember? If yes, it belongs in a `MEMORY.md`.
- **Test 3:** Is it specific to one workstation's domain? If yes, save it in that workstation's files. Only cross-cutting rules and facts go in the root files.

When unsure, suggest which file you think it belongs in and ask me to confirm.

**Memory hygiene** (the full rules are in `00_System/CONVENTIONS.md`):
- Keep entries to two sentences.
- A workstation's Current Status is a pointer of 80 words or fewer: state, blocker, next action, as of.
- Session narrative goes to that workstation's `<Workstation> Resources/Progress Log/Progress-Log.md`. A decision goes in full to `<Workstation> Resources/Progress Log/Decision-Log.md`, with one line in `MEMORY.md`.
- When something completes, propose moving its entry to `ARCHIVE.md` and move it once I confirm. `ARCHIVE.md` is reference-only: never read it at session start.
- Before a session that edited any `MEMORY.md` ends, run `python3 -B 00_System/Skills/workspace-audit/scripts/audit.py --warn-only` if Python is available, and fix or report what it flags.

**File naming:**
- Date-prefix (`YYYY-MM-DD-descriptive-name`) only immutable artifacts: reports, briefs, exports, anything that is finished when written.
- Living documents that get updated over time (checklists, indexes, trackers, reference files) get stable names without a date prefix, and a `Last updated: YYYY-MM-DD` line at the top.
- Dates are my local date (the timezone in `00_System/workspace-config.txt`), not the machine clock, which is often UTC. To get it: `TZ=<timezone> date +%F`.

## Task Tracking (`TASKS.md`)

The root `TASKS.md` is the index of task lists: one line per workstation pointing to its `[Workstation] Resources/Tracking/Tasks.md` (Active / Waiting On / Someday / Done). When a session creates or completes a to-do, update that workstation's task list in the same session. A to-do that belongs to no workstation goes directly in the root `TASKS.md`. When I ask what's on my plate, regenerate the dashboard first if Python is available (`00_System/Skills/work-dashboard/SKILL.md`), then read `TASKS.md` and `DASHBOARD.md`. Without Python, read each workstation's Current Status and task list directly.

## End of a session

When I say I'm wrapping up, or a working session ends:

1. Update each touched workstation's Current Status: 80 words or fewer, covering state, blocker, next action and as of.
2. Put session narrative in its Progress Log and decisions in its Decision Log (full text there, one line in `MEMORY.md`).
3. Update task lists and any `00_INDEX.md` whose folder changed, including its `Last updated` date.
4. If work is mid-flight, write a Session-Close Note (`00_System/Skills/session-handoff/SKILL.md`).
5. Regenerate the dashboard and run the audit with `--warn-only`. Without Python, use the by-hand checklist in `00_System/Skills/workspace-audit/SKILL.md`.

## Conventions (`00_System/CONVENTIONS.md`)

The full workspace conventions live in `00_System/CONVENTIONS.md` and carry the same authority as this file. Read the relevant section before creating, moving or renaming files, creating a workstation, or restructuring anything.

### File Placement & Folder Structure

Everything for a workstation lives in its `[Workstation] Resources/` folder, grouped into typed subfolders, with a `00_INDEX.md` kept current as part of every save. When you move or rename a file, rewrite every reference to it, and show me the moves first. Never delete anything without my explicit OK.

### The `00_System/` Folder

This is infrastructure and the audit trail (conventions, design notes, changelogs, the skills library), never domain content. Record every structural change there as a dated changelog.

### Creating New Workstations

Use the new-workstation skill (`00_System/Skills/new-workstation/SKILL.md`), then add a Routing Map row below.

### Nested Parent Workstations & Sub-Workstations

A sub-workstation is a full workstation that sits at its parent's root, beside the parent's Resources folder, never inside it, and routes as `Parent → Area`. Details: `00_System/CONVENTIONS.md`.

## Skills

Recurring operations have written procedures in `00_System/Skills/` (catalogue: `00_System/Skills/00_INDEX.md`). Before improvising a recurring operation, read the matching `SKILL.md`. Run scripts with `python3 -B`; they never delete or overwrite. If Python isn't available, follow the procedure by hand and say that you did.

## Preferences

_Set during first-run setup. Until then: plain, friendly language; concise answers; one clear recommendation unless I ask for options._

## Rules

- If you're not sure about something, say so. Don't guess.
- Before producing any written content on my behalf, read `00_Resources/voice-principles.md`.
- Show me any move, rename or archive before doing it. Never delete without my explicit OK.

## Routing Map

_When you start a task, check this table to decide which workstation applies. Add a row every time a workstation is created. Whether a workstation is Active, Dormant or Closed lives in `DASHBOARD.md` (set in `00_System/Skills/work-dashboard/lifecycle.txt`); a Closed workstation still routes, for history._

**When a task routes to a workstation:** read that workstation's `CLAUDE.md` (its rules file; every AI tool reads it, whatever the name) and `MEMORY.md` before doing any work there. Workstation rules layer on top of this file's rules; if they conflict, the workstation rule wins within its domain. If a task matches no row, work from the root files alone, and if it looks like the start of a recurring new domain, suggest creating a workstation for it.

| Workstation | Route here when I... |
|---|---|

## References

_Files in `00_Resources/` that load only when the trigger condition is met. Add rows as you create new reference files._

| Resource | Read when... |
|---|---|
| voice-principles.md | Writing any content on my behalf |
| profile.md | Personalizing responses, or when a task depends on who I am, what I do, or the tools I use |
