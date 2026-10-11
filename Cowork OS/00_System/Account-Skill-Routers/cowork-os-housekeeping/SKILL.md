---
name: cowork-os-housekeeping
description: Use in a Cowork OS folder for upkeep. Covers health checks and audits, what's-active dashboards, "remember this", memory that's getting long, archiving finished work, and whole-system reviews. Routes to the folder's own procedures.
---

# Cowork OS housekeeping

A thin router. The real procedures live in the Cowork OS folder under `00_System/Skills/`, and those `SKILL.md` files are the source of truth. Read the matching one and follow it exactly.

## Find the workspace first

The open or connected folder whose root holds `AGENTS.md`, `MEMORY.md` and `00_System/`. If it isn't reachable, say so and stop.

## Route

| Request | Read and follow |
|---|---|
| "Audit the workspace", a health check, or the end of a session that added or moved files or edited a `MEMORY.md` | `00_System/Skills/workspace-audit/SKILL.md` |
| "What's active?", "where does everything stand?", or a Current Status just changed | `00_System/Skills/work-dashboard/SKILL.md` |
| "Remember this", which file something belongs in, or a `MEMORY.md` over budget | `00_System/Skills/memory-maintenance/SKILL.md` |
| Something is confirmed done and its memory should move to `ARCHIVE.md` | `00_System/Skills/archive-helper/SKILL.md` |
| Optimize, review or rethink the whole system | Read `00_System/DESIGN-NOTES.md`, then `00_System/Skills/architecture-review/SKILL.md` |

## Rules that travel with every route

- Run scripts with `python3 -B`. If Python isn't available, follow the procedure by hand and say so.
- Show the owner any move, rename or archive before doing it. Never delete without their explicit OK.
