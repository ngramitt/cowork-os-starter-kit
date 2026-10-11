# Design Notes

Last updated: 2026-09-28 (living document; Cowork OS Starter Kit v1.0)

Why this workspace is built the way it is. Read this before changing the conventions or restructuring the whole workspace (the architecture-review skill starts here). Add to it when you make a design decision, so the next review builds on this one instead of starting over. The rules themselves live in the root `AGENTS.md` and `CONVENTIONS.md`; if this file and they disagree, they win and this file gets fixed.

This kit comes from a personal Cowork OS that ran for months before it was packaged. The decisions below are what that system learned the hard way.

## 1. The shape in one screen

- **What loads.** The AI reads the root `AGENTS.md` (rules and the Routing Map) and root `MEMORY.md`. The Routing Map sends each task to one workstation, whose `CLAUDE.md` (rules), `MEMORY.md` (state) and Resources `00_INDEX.md` (catalogue) are read next. Everything else is read on demand. Load cost is what the size budgets protect.
- **Five layers, one job each.** Rules go in `AGENTS.md` and workstation `CLAUDE.md` files. State is the `MEMORY.md` Current Status, 80 words or fewer. History goes in each workstation's Progress Log and Decision Log. Reference goes in Resources docs. Finished memory goes to `ARCHIVE.md`, which is never read at session start.
- **Generated, never hand-edited.** `DASHBOARD.md` comes from `dashboard.py`; audit reports come from `audit.py`. The root `TASKS.md` points to each workstation's task list.
- **Config that changes only on the owner's word:** `work-dashboard/lifecycle.txt`, `workspace-audit/budget-overrides.txt`, `workspace-audit/accepted-findings.txt` and `00_System/workspace-config.txt`.
- **Two tools, one rulebook.** The root rules live in `AGENTS.md`, which ChatGPT/Codex reads natively. `CLAUDE.md` imports it with an `@` import line, so Claude reads the same file. There is one copy, so there's nothing to keep in sync.

## 2. Decisions and why (don't undo one without a reason and the owner's yes)

| Decision | Why | Rejected |
|---|---|---|
| Current Status is 80 words or fewer: state, blocker, next action, as of | Long statuses get copied around and start contradicting each other. The original system found 10 contradictions before this rule. | Longer statuses; a hand-kept "active projects" list |
| One status source; the dashboard is generated from it | Removes the copy-and-drift problem | A hand-maintained dashboard |
| Content moves verbatim, leaves a pointer, and a script can prove nothing was lost | Summaries drop details you later need | Summarize and delete |
| Budgets are counted in words, not lines | A line cap was once met with 400-word lines | Line caps only |
| Budgets warn, never block; exceptions go per workstation, dated | Some workstations are reference-heavy by nature | Raising the global budget |
| Every workstation is born from one script template, with an index | Structure added after a pile forms never fully catches up | Creating folders by hand |
| The audit checks that every workstation has a routing row | A workstation without one is invisible to every session | Trusting the scaffold's printed reminder |
| Scripts are report-only or create-only | Automation never destroys anything | Scripts that move or delete |
| Confirm before any move, rename or archive; delete only on the owner's explicit word | Mistakes stay reversible | None |
| Closed workstations keep their folders and still route | History stays answerable | Moving or deleting closed folders |
| Dates use the owner's timezone (`workspace-config.txt`), not the machine clock | AI tools often run on UTC servers, which put evening work on tomorrow's date | The machine clock |
| Root rules in `AGENTS.md`, imported by `CLAUDE.md` | Claude and ChatGPT/Codex both work from one file | Two copies of the rules |
| Setup switches itself off by rewriting its own trigger | A trigger that stays on would re-run setup every session | Relying on the AI to remember that setup is done |
| Scheduled jobs must be cheap: the monthly audit is a two-step prompt | Each run spends the owner's usage | Heavy scheduled runs |
| File times are never set back to hide maintenance edits | Sync tools may treat an older time as a reason to restore old content | Touching file times |

## 3. Lessons from the original system

1. **Every individual save looked fine; the problem only showed up in aggregate.** Hygiene needs mechanical checks across the whole folder, not per-save judgment.
2. **Caps get met in ways that defeat them.** Measure what actually costs you (words, bytes), not a proxy.
3. **Copies drift.** Anything stated in two places will eventually contradict itself.
4. **Prose rules drift across sessions and models; scripts don't.** Even a careful system collects small inconsistencies. A "cold read" catches them: give a fresh AI session only the docs and see what it gets wrong.
5. **Structure has to exist at birth.**
6. **Measure before and after any big change.** Prove it's better; don't assume.

## 4. Known limits

- **Rules are guidance, not enforcement.** AI tools treat instruction files as context they try to follow. The real safety net is that you approve moves and deletes, and the audit reports drift afterward.
- **The dormancy clock resets on any `MEMORY.md` edit,** maintenance included. If a workstation shows as Active but isn't, mark it dormant in `lifecycle.txt`.
- **One owner, one writer.** This design assumes one person. Sharing a folder with others needs a different setup.
- **Nested instruction files are live.** If you ever store a copy of another Cowork OS (or any folder with its own `AGENTS.md` or `CLAUDE.md`) inside this one, your AI may read its instructions when it opens nearby files. Keep such copies zipped, or outside the workspace.
- **Load-cost figures are estimates** (bytes ÷ 4). Compare ratios, not absolutes.

## 5. Your changes

_Record your own design decisions here as you make them: what you changed, why, and what you rejected._
