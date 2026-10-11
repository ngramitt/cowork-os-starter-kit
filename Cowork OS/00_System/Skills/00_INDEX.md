# 00_INDEX: 00_System/Skills

_Last updated: 2026-10-11. The skills library: standardized procedures (`SKILL.md`) plus deterministic scripts that apply the root `AGENTS.md` conventions the same way across sessions, models and tools. Each skill is a folder with a `SKILL.md` and, where useful, a `scripts/` folder. Skills are living documents: stable names, "Last updated" lines, no date prefixes._

| Skill | Type | What it's for |
|---|---|---|
| `first-run-setup/` | 🟢 | Ten-minute first-run interview that personalizes the workspace, then switches itself off. `STARTER-IDEAS.md` is its menu of starter workstations. |
| `workspace-audit/` | 🟢 | Deterministic health check (`scripts/audit.py`): placement, indexes, references, size budgets, task hygiene, sync collisions, heavy folders, routing rows. Report-only. Holds `MONTHLY-AUDIT-PROMPT.md`, `budget-overrides.txt` and `accepted-findings.txt`. |
| `new-workstation/` | 🟢 | Scaffolds a workstation or sub-workstation exactly per template (`scripts/scaffold.py`). Never overwrites. |
| `memory-maintenance/` | 🟢 | Where new information goes (the three tests), status vs log, compression, archiving. |
| `work-dashboard/` | 🟢 | Regenerates the root `DASHBOARD.md` from every Current Status (`scripts/dashboard.py`); lifecycle overrides in `lifecycle.txt`. |
| `project-lifecycle/` | 🟢 | Spin-up → active → wrap → archive for any project. |
| `session-handoff/` | 🟢 | Session-Close Note and Handoff Brief (`HANDOFF-TEMPLATE.md`) for carrying work across sessions, models and tools. |
| `archive-helper/` | 🟢 | Prepares a `MEMORY.md` → `ARCHIVE.md` move as a plan (`scripts/prepare_archive.py`). Writes nothing. |
| `architecture-review/` | 🟢 | Whole-system review: `scripts/snapshot.py` measures, `scripts/verify_moves.py` proves a restructure lost nothing. |
| `SKILL-TEMPLATE.md` | 🟢 | How to write a new skill, plus the copy-paste template. |

_Legend: 🟢 living (update in place) · 📄 immutable (dated artifact)._

## Rules for skills in this folder

- A skill's `SKILL.md` restates root conventions as an exact procedure; the root `AGENTS.md` and `00_System/CONVENTIONS.md` stay the source of truth. If they diverge, fix the skill in the same session.
- Scripts are Python 3 standard library only, deterministic, and either report-only or create-only. Nothing here deletes, moves or overwrites existing files. Destructive steps always go through the owner.
- A new skill means a new subfolder, a row in this table and, if it should be found without being asked for, a row in the skills table in `00_System/CONVENTIONS.md`.
