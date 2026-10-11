---
name: project-lifecycle
description: The standard spin-up → active → wrap → archive procedure for any project in this workspace. Use when the owner starts something new ("new project", "let's start working on X"), when working sessions end, when a project's deliverable ships, or when the owner says a project is done.
---

# Project Lifecycle

Last updated: 2026-09-28 (living document; Cowork OS Starter Kit v1.0)

## What this is

Every project in this workspace passes through the same four stages. This
skill makes the transitions explicit so no stage is improvised: projects get
born with structure (not accreted), stay legible while active, and end with
their knowledge banked instead of rotting in a stale MEMORY.md. It composes
the other skills — new-workstation, work-dashboard, memory-maintenance,
workspace-audit — into one lifecycle; read their SKILL.md at the step that
invokes them.

## Stage 1 — Spin-up

1. **Decide the home.** Check the root AGENTS.md Routing Map:
   - Matches an existing workstation → the project is a **typed subfolder
     inside that workstation's Resources folder** (or uses the
     workstation's own project system if it has one, e.g. a
     `_PROJECT-TEMPLATE/` folder).
   - Matches nothing and looks like a recurring domain → propose a new
     workstation **[CONFIRM WITH OWNER]**, then run the new-workstation
     skill (never scaffold by hand).
2. **Define done.** One line in the project's driver doc or the
   workstation MEMORY.md: the deliverable, and what "finished" means. A
   project without a done-line becomes a zombie.
3. **Register it:** add the project to the workstation MEMORY.md Current
   Status (with the single next action), add any new subfolder to the
   Resources `00_INDEX.md`, and regenerate the dashboard (work-dashboard
   skill), which is where active work shows up.

## Stage 2 — Active (the session cadence)

At the END of every working session on the project:

1. Update the workstation MEMORY.md **Current Status to 2–3 lines + the
   single next action**. Progress detail, received documents, and running
   narrative go to a **progress log or dated artifact in Resources** —
   never accumulate in Current Status (that's how it bloats; see
   memory-maintenance).
2. New facts/decisions → the right file per the three tests
   (memory-maintenance skill).
3. If files were added/moved: update the relevant `00_INDEX.md`. If files
   moved or any MEMORY.md was edited, run `python3 -B 00_System/Skills/workspace-audit/scripts/audit.py --warn-only`.
4. Regenerate the dashboard if the status changed.

## Stage 3 — Wrap (deliverable ships)

Close-out checklist — all boxes, in order:

1. **File the deliverable** as a dated immutable artifact
   (`YYYY-MM-DD-...`) in the right typed subfolder; index it.
2. **Bank the knowledge:** decisions and their reasoning → the workstation
   MEMORY.md Key Decisions; anything reusable next time (a recipe, a
   contact, a gotcha) → the appropriate resource doc or a new one.
3. **Sweep:** run workspace-audit; nothing loose, nothing dangling,
   indexes current.
4. Set Current Status to "Complete — <deliverable> shipped <date>. Next
   action: none." and regenerate the dashboard.

## Stage 4 — Archive

When the owner confirms the project (or whole workstation) is finished
**[CONFIRM WITH OWNER — never archive on inference]**:

1. Move completed MEMORY.md entries → root `ARCHIVE.md` per the
   memory-maintenance skill (newest first, workstation-tagged, verbatim
   enough to answer future "what happened with X?" questions).
2. The workstation folder and its Routing Map row **stay** — archiving is
   about memory, not files. Only remove/retire a workstation if the owner
   explicitly asks **[CONFIRM WITH OWNER]**.
3. Regenerate the dashboard; the workstation should now show under Closed once it's marked closed in `work-dashboard/lifecycle.txt` (on the owner's word).

## What NOT to do

- Don't start work in a workstation root or Resources root "temporarily" — spin up the typed subfolder first (that's how piles form).
- Don't let Current Status become the progress log (Stage 2.1).
- Don't declare a project done without the Stage 3 checklist — an unshipped index or unbanked decision is invisible debt.
- Don't archive, delete, or retire anything without the owner's explicit confirmation.

## Editing this skill

If the root AGENTS.md conventions or the composed skills change, update the
step that references them in the same session.
