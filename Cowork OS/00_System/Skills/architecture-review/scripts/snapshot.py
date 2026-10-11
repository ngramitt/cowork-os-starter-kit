#!/usr/bin/env python3
"""Cowork OS system snapshot: load cost, memory size, lifecycle, tasks and audit
counts for the whole workspace, saved as JSON so a later review can compare.

Report-only / create-only: reads the workspace, writes one new JSON file under
../snapshots/ (never overwrites; adds -2, -3 ... if the date is taken).

Usage (from the workspace root):
  python3 -B 00_System/Skills/architecture-review/scripts/snapshot.py
  python3 -B .../snapshot.py --stdout                 # print only, write nothing
  python3 -B .../snapshot.py --compare .../snapshots/2026-09-27.json

Token figures are bytes / 4, a rough estimate: compare ratios, not absolutes.
"""
import json, os, re, subprocess, sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from pathlib import Path


def _load_local_tz():
    """The owner's timezone from 00_System/workspace-config.txt (written during
    first-run setup). Falls back to this machine's local timezone, so dates
    match the owner's calendar rather than a UTC server clock."""
    here = Path(__file__).resolve()
    for cand in here.parents:
        cfg = cand / "00_System" / "workspace-config.txt"
        if cfg.is_file():
            for line in cfg.read_text(encoding="utf-8").splitlines():
                key, _, val = line.partition("=")
                if key.strip().lower() == "timezone" and val.strip():
                    try:
                        return ZoneInfo(val.strip())
                    except Exception:
                        break
            break
    return datetime.now().astimezone().tzinfo


LOCAL_TZ = _load_local_tz()
NOW = datetime.now(LOCAL_TZ)   # the owner's local date, not the machine clock

HERE = Path(__file__).resolve().parent
SNAPDIR = HERE.parent / "snapshots"
SKILLS = HERE.parent.parent
STATUS_BUDGET, MEMORY_BUDGET = 80, 1200   # keep in step with workspace-audit/scripts/audit.py
DORMANT_DAYS = 60                          # keep in step with work-dashboard/scripts/dashboard.py


def find_root(start):
    p = Path(start).resolve()
    for c in [p, *p.parents]:
        if (c / "CLAUDE.md").exists() and (c / "MEMORY.md").exists() and (c / "00_System").is_dir():
            return c
    sys.exit("Run from inside the Cowork OS folder (needs root AGENTS.md, MEMORY.md, 00_System/).")


def tok(n): return round(n / 4)
def size(p): return p.stat().st_size if p.exists() else 0
def words(t): return len(t.split())


def section(text, heading):
    m = re.search(r"^## " + re.escape(heading) + r".*?\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1) if m else ""


def workstations(root):
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        d = Path(dirpath)
        dirnames[:] = [n for n in dirnames if not n.startswith((".", "_", "00_")) and not n.endswith(" Resources")]
        if d != root and "CLAUDE.md" in filenames and "MEMORY.md" in filenames:
            out.append(d)
    return sorted(out)


def read_pipe_file(path, ncols):
    rows = {}
    if path.exists():
        for line in path.read_text().splitlines():
            if line.strip() and not line.lstrip().startswith("#"):
                parts = [x.strip() for x in line.split("|")]
                if len(parts) >= ncols:
                    rows.setdefault(parts[0], []).append(parts[1:])
    return rows


def audit_counts(root):
    script = SKILLS / "workspace-audit" / "scripts" / "audit.py"
    if not script.exists():
        return None
    r = subprocess.run([sys.executable, "-B", str(script), str(root)], capture_output=True, text=True, cwd=root)
    g = lambda pat: int(m.group(1)) if (m := re.search(pat, r.stdout)) else 0
    return {"warn": g(r"## WARN \((\d+)\)"), "info": g(r"## INFO \((\d+)\)"), "total": g(r"Total: (\d+)")}


def build(root):
    start = size(root / "AGENTS.md") + size(root / "CLAUDE.md") + size(root / "MEMORY.md")
    dash = (root / "DASHBOARD.md").read_text() if (root / "DASHBOARD.md").exists() else ""
    life = read_pipe_file(SKILLS / "work-dashboard" / "lifecycle.txt", 2)
    over = read_pipe_file(SKILLS / "workspace-audit" / "budget-overrides.txt", 3)
    rows, agree, have_next = [], 0, 0
    for ws in workstations(root):
        rel = ws.relative_to(root).as_posix(); label = rel.replace("/", " → ")
        mem = (ws / "MEMORY.md").read_text(); status = section(mem, "Current Status")
        res = ws / f"{ws.name} Resources"; state = res / "STATE.md"; tasks = res / "Tracking" / "Tasks.md"
        budgets = {k: int(v) for k, v, *_ in over.get(rel, []) if v.isdigit()}
        nxt = re.search(r"(?i:next action)s?\s*[:\-]\s*(.{10,60})", status.replace("**", ""))
        in_dash = None
        if nxt:
            first = re.split(r"(?<=[.;!?])\s", nxt.group(1).strip())[0]   # the dashboard stops at the first sentence end
            have_next += 1; in_dash = first[:40] in dash; agree += in_dash
        age = int((NOW.timestamp() - (ws / "MEMORY.md").stat().st_mtime) // 86400)
        state_ = life[label][0][0].lower() if label in life else ("dormant" if age > DORMANT_DAYS else "active")
        rows.append({
            "workstation": rel,
            "lifecycle": state_,
            "days_since_memory_change": age,
            "load_tokens": tok(start + size(ws / "CLAUDE.md") + size(ws / "MEMORY.md") + size(state)),
            "claude_kb": round(size(ws / "CLAUDE.md") / 1024, 1),
            "memory_words": words(mem), "memory_budget": budgets.get("memory_words", MEMORY_BUDGET),
            "status_words": words(status), "status_budget": budgets.get("status_words", STATUS_BUDGET),
            "lines_over_60_words": sum(1 for l in mem.splitlines() if len(l.split()) > 60),
            "open_tasks": len(re.findall(r"(?m)^\s*- \[ \]", tasks.read_text())) if tasks.exists() else None,
            "has_progress_log": (res / "Progress Log" / "Progress-Log.md").exists(),
            "next_action_on_dashboard": in_dash,
        })
    nfiles = nbytes = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [n for n in dirnames if not n.startswith(".")]
        for f in filenames:
            if not f.startswith("."):
                nfiles += 1; nbytes += size(Path(dirpath) / f)
    loads = [r["load_tokens"] for r in rows]
    active = [r["load_tokens"] for r in rows if r["lifecycle"] == "active"]
    return {
        "date": NOW.strftime("%Y-%m-%d"), "method": "tokens = bytes / 4; workstation load = root AGENTS.md + CLAUDE.md + root MEMORY.md + workstation CLAUDE.md + MEMORY.md + Resources/STATE.md if present",
        "scenarios": {
            "session_start": tok(start),
            "whats_on_my_plate": tok(start + size(root / "TASKS.md") + size(root / "DASHBOARD.md")),
            "avg_workstation": round(sum(loads) / len(loads)) if loads else 0,
            "avg_active_workstation": round(sum(active) / len(active)) if active else 0,
            "max_workstation": max(loads) if loads else 0,
        },
        "root": {"claude_kb": round((size(root / "AGENTS.md") + size(root / "CLAUDE.md")) / 1024, 1), "memory_words": words((root / "MEMORY.md").read_text()),
                 "tasks_kb": round(size(root / "TASKS.md") / 1024, 1), "dashboard_kb": round(size(root / "DASHBOARD.md") / 1024, 1)},
        "workspace": {"workstations": len(rows), "files": nfiles, "mb": round(nbytes / 2**20, 1),
                      "lifecycle": {s: sum(r["lifecycle"] == s for r in rows) for s in ("active", "dormant", "closed")}},
        "dashboard_next_action_agreement": f"{agree}/{have_next}",
        "audit": audit_counts(root),
        "workstation_rows": rows,
    }


def show(s):
    print(f"Cowork OS snapshot {s['date']}  ({s['workspace']['workstations']} workstations, {s['workspace']['files']} files, {s['workspace']['mb']} MB)")
    for k, v in s["scenarios"].items():
        print(f"  {k:<24} ~{v:,} tokens")
    print(f"  lifecycle {s['workspace']['lifecycle']}  dashboard agreement {s['dashboard_next_action_agreement']}  audit {s['audit']}")
    for r in s["workstation_rows"]:
        flags = []
        if r["memory_words"] > r["memory_budget"]: flags.append(f"memory {r['memory_words']}/{r['memory_budget']}")
        if r["status_words"] > r["status_budget"]: flags.append(f"status {r['status_words']}/{r['status_budget']}")
        if r["next_action_on_dashboard"] is False: flags.append("dashboard stale")
        if flags: print(f"  ! {r['workstation']}: " + ", ".join(flags))


def compare(old, new):
    print(f"\nCompare {old['date']} -> {new['date']}")
    for k in new["scenarios"]:
        a, b = old["scenarios"].get(k), new["scenarios"][k]
        if a: print(f"  {k:<24} {a:>7,} -> {b:>7,}  ({(b - a) / a:+.0%})")
    o = {r["workstation"]: r for r in old["workstation_rows"]}; n = {r["workstation"]: r for r in new["workstation_rows"]}
    for w in sorted(set(o) | set(n)):
        if w not in o: print(f"  + {w} (new, ~{n[w]['load_tokens']:,} tokens)")
        elif w not in n: print(f"  - {w} (gone)")
        elif o[w]["load_tokens"] and abs(n[w]["load_tokens"] - o[w]["load_tokens"]) / o[w]["load_tokens"] >= 0.15:
            print(f"  ~ {w}: {o[w]['load_tokens']:,} -> {n[w]['load_tokens']:,} tokens")
    print(f"  audit {old.get('audit')} -> {new.get('audit')}")


if __name__ == "__main__":
    args = sys.argv[1:]
    root = find_root(next((a for a in args if not a.startswith("--") and not a.endswith(".json")), "."))
    snap = build(root); show(snap)
    if "--compare" in args:
        compare(json.loads(Path(args[args.index("--compare") + 1]).read_text()), snap)
    if "--stdout" not in args:
        SNAPDIR.mkdir(exist_ok=True)
        out, i = SNAPDIR / f"{snap['date']}.json", 2
        while out.exists():
            out, i = SNAPDIR / f"{snap['date']}-{i}.json", i + 1
        out.write_text(json.dumps(snap, indent=1, ensure_ascii=False))
        print(f"\nWrote {out.relative_to(root)}")
