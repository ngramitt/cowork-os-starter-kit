---
name: memory-maintenance
description: Standard procedure for keeping MEMORY.md files healthy — where to save new information (the three tests), how to compress, and how to archive completed items to ARCHIVE.md. Use when the owner says "remember this", when a MEMORY.md exceeds 150 lines, when a project completes, or when the workspace-audit flags a memory cap.
---

# Memory Maintenance

Last updated: 2026-09-28 (living document; Cowork OS Starter Kit v1.0)

## What this is

The memory rules from the root `AGENTS.md`, restated as an exact procedure
so every agent (any model, any session) applies them identically. The root
`AGENTS.md` and `00_System/CONVENTIONS.md` remain the source of truth; if it and this file disagree, the
root file wins — and fix this file in the same session.

## Saving new information — the three tests, in order

1. **Does it prescribe behavior?** ("always", "never", "before X do Y") →
   a `CLAUDE.md`, under the appropriate section.
2. **Is it a fact about the world that could change?** (contacts, status,
   decisions) → a `MEMORY.md`.
3. **Is it specific to one workstation's domain?** → that workstation's
   file. Only cross-cutting rules/facts go in the root files.

When unsure, suggest a file and ask the owner to confirm. When the owner says
"remember this", write it immediately and confirm you did.

**Entry format:** two sentences max per entry. Facts and status in plain
declarative sentences; decisions include the one-line reasoning.

## Status vs. log — the anti-bloat rule

Current Status is a **pointer, not a story**: 2–4 bullets (state, blocker,
next action) linking to where detail lives. Dated narrative entries,
received-record write-ups, and correspondence outcomes belong in a
**`Progress Log/Progress-Log.md`** inside the workstation's Resources
(newest first) (the project-lifecycle and session-handoff skills show how
it's used). When consolidating, move entries **verbatim** and
leave a pointer; never summarize-and-delete. Nothing that represents real
progress or evidence is ever lost — when in doubt, move rather than remove,
and note in the file where it went.

## The 150-line cap — compression pass

Every MEMORY.md (root and workstation) stays under 150 lines. When one
exceeds it, in this order:

1. **Compress verbose entries** — tighten to the two-sentence cap, merge
   duplicates, drop restated context that lives in CLAUDE.md.
2. **Archive completed/outdated items** (next section) only if compression
   isn't enough.
3. Never delete Current Status, active contacts, or working conventions —
   current-state content stays regardless of age.

## Archiving to ARCHIVE.md

When a project completes or an entry becomes outdated:

1. Cut the entry from its MEMORY.md.
2. Append it to the root `ARCHIVE.md` **below the marker line, newest
   first**, using the format: `## [Topic] (archived YYYY-MM-DD)` — and tag
   the workstation name if it came from one, e.g.
   `## [Job Search] Final offer decision (archived 2026-11-02)`.
3. Keep the archived text verbatim enough that a future "what happened
   with X?" question can be answered from ARCHIVE.md alone.
4. If the whole *project* completed (not just an entry), also update the
   workstation's MEMORY.md Current Status to say so and regenerate the
   dashboard.

**ARCHIVE.md is reference-only:** never read it at session start; open it
only when the owner asks about something historical.

## Before the session ends

After any MEMORY.md edit, run `python3 -B 00_System/Skills/workspace-audit/scripts/audit.py --warn-only` if Python is available; otherwise do the by-hand checklist in `00_System/Skills/workspace-audit/SKILL.md`. It prints only the warnings (size budgets, missing indexes, collisions) and a count of the rest, so it costs a few hundred tokens. Fix what it flags, or tell the owner. Per-workstation budget exceptions live in `00_System/Skills/workspace-audit/budget-overrides.txt` and change only on the owner's word.

## What NOT to do

- Don't archive anything ambiguous without asking — "looks done" isn't done
  (a finished project's final outcome waits *pending the owner's
  go-ahead* before archiving; that pending state is the norm).
- Don't rewrite history in ARCHIVE.md; it's append-only.
- Don't let MEMORY.md accumulate session narration — it stores facts and
  decisions, not a diary.
