# HANDOFF-TEMPLATE — copy for every Handoff Brief

Last updated: 2026-09-28 (living document; Cowork OS Starter Kit v1.0)
`session-handoff/SKILL.md` — read that first. Copy from the line below into
`<Workstation>/<Workstation> Resources/Handoffs/YYYY-MM-DD-Handoff - <topic>.md`,
fill every bracket, delete instruction comments. Write for a cold-start
agent on any model.

---

# Handoff Prompt — [Topic]

_Paste everything below the line into a fresh session (Claude or ChatGPT). It is written to
you, the executing agent — whichever model you are — and is self-contained:
it tells you where you are, what is already decided, and what to deliver._

---

You are picking up the **[Workstation]** workstation inside the owner's Cowork
OS. [1–3 sentences: what prior sessions accomplished, and the job this
handoff delegates.]

## 0. Orient yourself first (before proposing anything)

Read these in order, then summarize the current state back to the owner before
you build:

1. `AGENTS.md` and `MEMORY.md` at the workspace root (root rules + memory).
2. `[Workstation]/CLAUDE.md` and `[Workstation]/MEMORY.md`.
3. `00_Resources/voice-principles.md` (before writing anything in the owner's voice) and `00_Resources/profile.md`.
4. [The source-of-truth files for this work — exact paths, one line each on why.]

Follow every workspace rule: outline your plan and get approval before any
large build; ask clarifying questions first; confirm before
deleting/overwriting/renaming; `YYYY-MM-DD-` names for new immutable
artifacts; update the relevant `00_INDEX.md` when you file anything; follow the owner's Preferences in the root `AGENTS.md`. [Add the workstation's own binding
constraints here — gates, thresholds, editorial rules.]

## 1. Context that is settled (do not relitigate)

[Bullet the decided facts and decisions this work builds on. Link the doc
that settled each. If a fresh agent would be tempted to reopen something,
say explicitly that it is closed and why.]

## 2. What you must deliver

[Numbered deliverables. For each: what it is, where it gets filed (typed
subfolder), and what standard it must meet.]

## 3. Open questions to put to the owner before you build

[Numbered, genuinely open questions only. If the answer exists in a doc,
it belongs in Section 1, not here.]

## 4. What "done" looks like

[One paragraph: the finished state, including which `00_INDEX.md` rows and
which MEMORY.md Current Status update count as part of done.]

Start by orienting yourself (Section 0), answer the Section 3 questions
with the owner, then tell the owner your plan.
