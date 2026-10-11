---
name: architecture-review
description: Whole-system review and optimization of the Cowork OS. Measures it, finds drift, plans changes in gated phases, moves content without losing any, and proves the result is better. Use when the owner asks to optimize, review, clean up or rethink the whole workspace or its CLAUDE.md/MEMORY.md system, asks how it compares with other setups, or at a yearly check-up.
---

# Architecture Review

Last updated: 2026-09-28 (living document; Cowork OS Starter Kit v1.0)

## What this is

This is the procedure the original Cowork OS used for its first whole-system review (September 2026). Each review should start from the last one's findings instead of from scratch. **Read `00_System/DESIGN-NOTES.md` first.** It holds the design decisions and why they were made, the known weak spots, and the numbers to beat. This skill composes workspace-audit, work-dashboard, memory-maintenance and archive-helper; it does not replace them.

## When to run

- The owner asks to optimize, review, clean up or rethink the whole system, not just one workstation.
- The owner asks how the setup compares with other people's.
- About once a year, or when the workspace has grown a lot since the newest file in `snapshots/`.

## Procedure

1. **Orient cheaply.** Read `00_System/DESIGN-NOTES.md`, `00_System/ROADMAP.md` and the newest changelogs in `00_System/`. Don't open every workstation yet.
2. **Measure.** From the workspace root run `python3 -B 00_System/Skills/architecture-review/scripts/snapshot.py --compare <newest file in 00_System/Skills/architecture-review/snapshots/>`, then `python3 -B 00_System/Skills/workspace-audit/scripts/audit.py`. The snapshot writes a new dated JSON, and the comparison shows what grew.
3. **Ask the owner before planning.** Use your tool's multiple-choice questions if it has them. Start with the open questions and weak spots recorded in DESIGN-NOTES.
4. **Research outside patterns only when asked, or if a year has passed.** Re-check any outside sources DESIGN-NOTES cites, because they change. Compare them; don't copy them.
5. **Plan in gated phases** and put the plan where the owner can read and comment on it, such as a shared document they can comment on. The order that worked:
   1. Tooling and checks, with no content moves.
   2. Move narrative out of memory.
   3. Slim the root layer.
   4. Lifecycle and archiving.
   5. Test.

   Each phase starts only after the owner says yes. **[CONFIRM WITH OWNER]**
6. **Move content safely** in any phase that edits existing files.
   - Back up each file **outside** the workspace first (for example `~/bak/<phase>/`, with distinct names, using `cp -p`). A backup inside the workspace gets synced and clutters it.
   - Build the new text in a script. Use exact-match replacements that fail unless the old text appears exactly once. Check the staged text before writing.
   - Run `python3 -B 00_System/Skills/architecture-review/scripts/verify_moves.py BACKUP=CURRENT ...`. Every line it reports as missing must be one you edited on purpose; list those lines in the changelog.
   - Moves are verbatim and leave a pointer behind. Never summarize and delete. Use `mv -n`. Delete only on the owner's explicit word.
7. **Close each phase:**
   - a dated changelog in `00_System/`, using the owner's local date;
   - index rows and Last updated lines;
   - `dashboard.py`, then `audit.py --warn-only`;
   - confirm `find . -name __pycache__` returns nothing.
8. **Prove it's better.** Run `snapshot.py --compare` against the snapshot from step 2. Re-run any contradiction checks you wrote in steps 2 and 3. Write a dated test report (nothing lost, load cost before and after, contradictions, integrity, limits). Say plainly what the test can't show.
   - **Cold read.** Give a fresh agent only the changed docs: root `AGENTS.md`, `CONVENTIONS.md`, and the skills and scripts. Have it answer routing and placement questions citing sections, cross-check numbers and references between files, and run the scripts, including breaking things on a copy. List what it gets wrong or finds ambiguous, and fix it before closing the review. The first cold read of the original system found four real drift issues.
9. **Leave it better for next time.** Update DESIGN-NOTES (decisions, weak spots, numbers), the ROADMAP, and this skill if the procedure changed.

## What NOT to do

- Don't undo a decision in DESIGN-NOTES without saying why and getting the owner's yes.
- Don't set file modification times back to hide maintenance edits. A cloud sync tool may treat the older time as a reason to restore the old content. Use `lifecycle.txt` instead.
- Don't raise the global budgets to quiet one workstation. Use `budget-overrides.txt`, on the owner's word.
- Don't add scheduled or recurring jobs without estimating their cost per run. Treat that cost as a real constraint.
- Don't touch `.DS_Store` files.

## Editing this skill

The budgets and the dormancy threshold are constants at the top of `scripts/snapshot.py`. Keep them in step with `workspace-audit/scripts/audit.py` and `work-dashboard/scripts/dashboard.py`. Snapshots are dated JSON files in `snapshots/`, and a new one never overwrites an old one.
