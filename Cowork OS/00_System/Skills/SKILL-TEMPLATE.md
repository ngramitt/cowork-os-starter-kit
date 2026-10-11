# SKILL-TEMPLATE — how to author a new workspace skill

Last updated: 2026-09-28 (living document; Cowork OS Starter Kit v1.0)
`00_System/Skills/<skill-name>/SKILL.md` when creating a new skill. Keeping
every skill in this shape is what lets any agent or model pick one up cold.

## Authoring rules

1. **One skill = one recurring operation.** If the SKILL.md needs two "When
   to run" sections, it's two skills.
2. **Deterministic before clever.** If a step can be a Python 3 stdlib
   script, make it one (in `scripts/`). Scripts must be report-only or
   create-only — never delete, move, or overwrite existing files. Anything
   destructive stays a human-confirmed step in the procedure text.
3. **Restate, don't replace.** Skills restate root-AGENTS.md conventions as
   exact procedure; the root file stays the source of truth. If they
   diverge, fix the skill in the same session.
4. **Write for a cold start.** Assume the executing agent has read nothing
   but the root AGENTS.md. Name exact paths, exact commands, exact output
   expectations. No "as discussed" or session-relative references.
5. **Register it twice:** a row in `00_System/Skills/00_INDEX.md`, and — if
   agents must discover it unprompted — a row in the skills table in
   `00_System/CONVENTIONS.md` with a precise "Use when..." trigger.
6. **Test before registering.** Run scripts against a temp copy or with
   report-only output; paste nothing into the workspace that hasn't run.
7. Skills are living documents: stable folder name (kebab-case), "Last
   updated:" line, no date prefix.

## Template (copy from here down)

```markdown
---
name: <skill-name>
description: <One sentence: what it does. One sentence: the exact trigger phrases/situations to use it.>
---

# <Skill Name>

Last updated: YYYY-MM-DD (living document)

## What this is

<2-4 lines: the operation this standardizes and why it exists (link the
convention or post-mortem it enforces).>

## When to run

<Bullet list of concrete triggers.>

## Procedure

<Numbered steps. Exact paths and commands. Mark any step that needs the owner's
confirmation with **[CONFIRM WITH OWNER]**.>

## What NOT to do

<The failure modes this skill exists to prevent.>

## Editing this skill

<Where the knobs live; what to update when conventions change.>
```
