---
name: cowork-os-project-flow
description: Use in a Cowork OS folder to create a workstation, start or wrap up a project, end a session with work still in progress, or write a handoff for a fresh session or another AI tool. Routes to the folder's own procedures.
---

# Cowork OS project flow

A thin router. The real procedures live in the Cowork OS folder under `00_System/Skills/`, and those `SKILL.md` files are the source of truth. Read the matching one and follow it exactly.

## Find the workspace first

The open or connected folder whose root holds `AGENTS.md`, `MEMORY.md` and `00_System/`. If it isn't reachable, say so and stop.

## Route

| Request | Read and follow |
|---|---|
| Create a workstation or sub-workstation, or a task fits no Routing Map row and looks like a recurring new area | `00_System/Skills/new-workstation/SKILL.md` (confirm the name first) |
| Start a project, end a working session on one, a deliverable ships, or the owner says something is done | `00_System/Skills/project-lifecycle/SKILL.md` |
| "Write a handoff", "prep this for a fresh session", or ending a session with work mid-flight | `00_System/Skills/session-handoff/SKILL.md` |

## Rules that travel with every route

- Before working in a workstation, check the Routing Map in the root `AGENTS.md`, then read that workstation's `CLAUDE.md` and `MEMORY.md`.
- Current Status stays within 80 words (state, blocker, next action, as of). Session narrative goes to the Progress Log.
- Show the owner any move, rename or archive before doing it. Never delete without their explicit OK.
