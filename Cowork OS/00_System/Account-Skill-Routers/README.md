# Account Skill Routers (optional)

Last updated: 2026-09-28 (living document; Cowork OS Starter Kit v1.0)

Three small skills you can add to your Claude or ChatGPT account. They don't contain any procedures themselves; they just point your AI at the procedures inside this folder. Once they're installed, requests like "audit my workspace" or "write a handoff" get recognized even when you phrase them casually. You don't need them: the rules in `AGENTS.md` already tell your AI where the procedures live.

| Skill | What it catches |
|---|---|
| `cowork-os-start` | Opening the workspace, catching up ("what's on my plate?"), unfinished setup |
| `cowork-os-housekeeping` | Audits, the dashboard, "remember this", archiving, whole-system reviews |
| `cowork-os-project-flow` | New workstations, projects, handoffs |

They use the open Agent Skills format (a folder with a `SKILL.md`), which both Claude and ChatGPT support.

## Installing

Menus change, so if a step doesn't match what you see, ask your AI: "Help me install the three skills in `00_System/Account-Skill-Routers`."

- **Claude:** in Claude's settings, find the Skills section and upload each skill as a zip of its folder (for example, a zip of `cowork-os-start/`).
- **ChatGPT desktop app or Codex:** copy the three folders into `~/.agents/skills/` in your home folder. That's where Codex and ChatGPT look for your personal skills. You can also add skills from ChatGPT's own skills settings, if your plan shows them.

## Updating

If you change a procedure in `00_System/Skills/`, the routers don't need to change. They only point at the procedures. Update a router only if you rename or add a skill.
