# Monthly structure audit: scheduled-task prompt

Last updated: 2026-09-28 (living document; Cowork OS Starter Kit v1.0)

This is the prompt for an optional monthly structure-audit scheduled task in your AI tool. Claude's desktop app and ChatGPT both offer scheduled tasks on some plans. First-run setup offers to create it. The checks live in `scripts/audit.py`, not in the prompt, so the prompt stays two steps long and every month runs the same checks on any model. If a root `AGENTS.md` convention changes, change the script and this skill's `SKILL.md`, never the prompt.

Paste everything between the lines into the scheduled task:

---

Run the monthly Cowork OS structure audit. It is read-only: change, move, rename and delete nothing. Keep it cheap: run the two scripts and report from their output; don't open workstation files.

1. In the connected Cowork OS folder, run `python3 -B 00_System/Skills/workspace-audit/scripts/audit.py` and `python3 -B 00_System/Skills/work-dashboard/scripts/dashboard.py --stdout`. Both find the workspace root on their own; `-B` keeps them from leaving `__pycache__` behind. If the folder isn't connected or a script fails, say so in one line and stop.
2. Report in under 300 words: "All clean" if the audit exits 0; otherwise the WARN findings grouped by workstation with the fix each needs (see "How to act on the report" in `00_System/Skills/workspace-audit/SKILL.md`; the conventions it enforces are in `00_System/CONVENTIONS.md`), one line counting the INFO findings, and any Dormant workstation on the dashboard that looks finished. Then ask the owner which fixes to apply and wait. Budget fixes follow `00_System/Skills/memory-maintenance/SKILL.md`: move narrative verbatim to the workstation's Progress Log, never trim.

---
