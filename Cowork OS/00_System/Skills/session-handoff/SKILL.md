---
name: session-handoff
description: Standard procedure for handing work between sessions and agents — a full Handoff Brief for delegating a chunk of work to a fresh session, and a short Session-Close Note for ending any working session warm. Use when the owner says "write a handoff", "prep this for a fresh session", "package this up for next time", or at the end of any working session where meaningful work is mid-flight.
---

# Session Handoff

Last updated: 2026-09-28 (living document; Cowork OS Starter Kit v1.0)

## What this is

Sessions are stateless and may run on different models or tools (Claude,
ChatGPT, others). Work that lives only in a session's context dies with it. This
skill standardizes the two artifacts that carry work across that boundary,
keeping each brief in a `Handoffs/` subfolder of the owning workstation's
Resources. It slots into project-lifecycle
Stage 2.

**Write every handoff for the weakest plausible reader: a cold-start agent
on a different model that has read nothing but the root AGENTS.md.** If the
brief only works because the writer remembers the session, it has failed.

## The two artifacts

| Artifact | When | Where it lives |
|---|---|---|
| **Handoff Brief** | Delegating a defined chunk of work to a fresh session (big builds, parallel workstreams, "pick this up tomorrow") | Dated immutable artifact (`YYYY-MM-DD-Handoff - <topic>.md`) in a `Handoffs/` typed subfolder of the owning workstation's Resources; add it to that `00_INDEX.md` |
| **Session-Close Note** | End of ANY working session with mid-flight work, even without a planned delegation | Newest-first entry in the workstation's `Progress Log/Progress-Log.md` (create the log per memory-maintenance if absent), plus the normal 2–3-line MEMORY.md Current Status refresh |

## Procedure — Handoff Brief

Copy `HANDOFF-TEMPLATE.md` (next to this file) and fill every section.
Rules that make it survive the model boundary:

1. **Address the reader as "you", model-neutrally.** Not "Claude will…" or
   "ChatGPT will…": the next agent may be a different model or tool. Title the file `…-Handoff - <topic>.md`
   (no model names in file names).
2. **Section 0 is an ordered orient-first reading list** with exact paths
   from the workspace root: root `AGENTS.md`/`MEMORY.md`, the workstation's
   `CLAUDE.md`/`MEMORY.md`, `00_Resources/voice-principles.md`, then the
   source-of-truth files for the work. Instruct the reader to summarize
   state back to the owner before building.
3. **Settled vs. open, explicitly.** A "do not relitigate" section for
   decided things (with the deciding doc linked), and a numbered
   "questions for the owner" section for genuinely open ones. The single worst
   handoff failure is a fresh agent reopening settled decisions.
4. **One done-line.** What finished looks like, including which
   `00_INDEX.md` and MEMORY.md updates count as part of done.
5. **Restate the binding constraints inline** (gates, margins, editorial
   rules, confirm-first rules) rather than assuming they'll be inferred —
   repetition across the boundary is cheap; drift is not.
6. Register the brief in the workstation's `Handoffs/00_INDEX.md` (create
   the subfolder + index on first use). When a brief is executed, mark its
   index row "EXECUTED (now historical)".

## Procedure — Session-Close Note

At the end of a working session with mid-flight work, append to the
workstation's Progress Log (newest first), under a `## YYYY-MM-DD — Session
close` heading, exactly five parts:

1. **Done this session** — what shipped/changed, with paths.
2. **Mid-flight** — what's half-built and where it stands.
3. **Next action** — the single next step (mirror it in Current Status).
4. **Decisions made** — one line each, with reasoning (also bank per
   memory-maintenance if durable).
5. **Traps for the next agent** — anything a cold reader would plausibly
   get wrong (stale docs, superseded numbers, "looks done but isn't").

Then finish the normal Stage-2 cadence: MEMORY.md Current Status refresh,
index updates, workspace-audit (`--warn-only`) if files moved or a MEMORY.md was edited, dashboard regen if status
changed.

## When the next session can't open this folder

If the work continues in a plain chat that can't see this folder (for example a ChatGPT or Claude conversation without the folder attached), write the brief as usual. Then add a final instruction to it: "When you finish, end with a short summary I can paste back." When the owner brings that summary back, file it as a Session-Close Note in the workstation's Progress Log and update Current Status.

When a session touched several workstations, write a Session-Close Note in each one that has work mid-flight.

## What NOT to do

- Don't write handoffs that require the reader to have been in the session ("as discussed", "the file from earlier").
- Don't put the handoff's content in MEMORY.md — Current Status stays a 2–3-line pointer; the brief/note carries the detail.
- Don't skip the Session-Close Note because a Handoff Brief exists for part of the work — the note covers the whole session.
- Don't let a fresh agent execute a brief without the Section-0 orient step.

## Editing this skill

The template lives in `HANDOFF-TEMPLATE.md` next to this file. If the
project-lifecycle or memory-maintenance procedures change, update the
steps that reference them in the same session.
