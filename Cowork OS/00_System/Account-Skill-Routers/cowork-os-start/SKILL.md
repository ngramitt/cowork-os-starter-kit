---
name: cowork-os-start
description: Use whenever a conversation has a Cowork OS folder open (a folder with AGENTS.md, MEMORY.md and 00_System/ at its root) and the person wants to work in it, catch up ("what's on my plate?"), or finish setting it up. Orients in the workspace before doing anything else.
---

# Cowork OS: start here

A thin router. The real procedures live inside the person's Cowork OS folder, and those files are the source of truth.

## Find the workspace

- It's the open or connected folder whose root holds `AGENTS.md`, `MEMORY.md` and `00_System/`.
- If no such folder is reachable in this conversation, say so in one line and suggest opening the folder (in local mode on ChatGPT). Don't rebuild the system from memory.

## Then

1. Read the root `AGENTS.md` and follow it. If its **Setup status** says "Not set up yet," run `00_System/Skills/first-run-setup/SKILL.md`.
2. Read the root `MEMORY.md`.
3. For "what's on my plate?", read `TASKS.md` and `DASHBOARD.md`. If Python is available, regenerate the dashboard first (`00_System/Skills/work-dashboard/SKILL.md`).
4. Otherwise, route the request with the Routing Map in `AGENTS.md`, and read that workstation's `CLAUDE.md` and `MEMORY.md` before working.
