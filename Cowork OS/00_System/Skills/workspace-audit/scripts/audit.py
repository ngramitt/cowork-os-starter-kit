#!/usr/bin/env python3
"""
Cowork OS workspace audit — deterministic health check.

Checks the workspace against the conventions in the root AGENTS.md
("File Placement & Folder Structure", memory hygiene rules, naming rules).
REPORT-ONLY: this script never moves, renames, or deletes anything.
Every finding is a flag for a human/agent to review — per the owner's global
rule, nothing is deleted/moved without showing the owner first.

Usage:
    python3 audit.py [WORKSPACE_ROOT]

If WORKSPACE_ROOT is omitted, the script walks up from its own location
to find the workspace root (the directory containing CLAUDE.md, MEMORY.md
and 00_System/).

    python3 audit.py [WORKSPACE_ROOT] --warn-only   # WARNs in full, INFO as a count

Exit code: 0 = clean, 1 = findings, 2 = couldn't locate workspace root.

Size
budgets (MEMORY.md words, Current Status words, long lines, CLAUDE.md bytes,
STATE.md lines), TASKS.md hygiene, " (1)" sync-collision names and heavy
build folders; cut false positives in the dangling-reference check. Budgets
WARN or INFO, they never block. All thresholds live in the config below.

2026-09-28: added check 13 (routing). Every workstation needs a routing row
(the root Routing Map, or its parent's Sub-Routing Map / Sub-Areas table), and
every routing row must point at a real workstation. scaffold.py prints the
row to add, but until now nothing verified that it was added.
"""

import os
import re
import sys
from datetime import date, datetime
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
from pathlib import Path

# ---------------------------------------------------------------- config

MEMORY_LINE_CAP = 150          # root AGENTS.md memory hygiene rule #2

# Size budgets (added 2026-09-27). A line cap alone can be met with very long
# lines, so memory is also measured in words. Tune after a monthly cycle.
MEMORY_WORD_BUDGET = 1200      # words per MEMORY.md
STATUS_WORD_BUDGET = 80        # words in a MEMORY.md "Current Status" section
LINE_WORD_CAP = 60             # words on any single MEMORY.md line
ROOT_CLAUDE_BYTES = 11 * 1024  # root AGENTS.md, loaded into every session.
                               # (the root AGENTS.md in the Starter Kit)
WS_CLAUDE_BYTES = 10 * 1024    # a workstation CLAUDE.md
STATE_LINE_CAP = 40            # STATE.md driver docs ("forty lines")
TASK_WORD_CAP = 25             # words per TASKS.md item
TASK_ACTIVE_CAP = 20           # open items in TASKS.md "Active"
HEAVY_DIR_MB = 20              # build/cache/"_" folders above this get listed
HEAVY_DIR_NAMES = {"build", "cache", "tmp", "ocr", "images_final"}  # exact names
# Google Drive / macOS name collisions: "name (1).ext", "folder (2)"
COLLISION_RE = re.compile(r"^(?P<stem>.+) \((?P<n>\d+)\)(?P<ext>\.[A-Za-z0-9]+)?$")
# Template placeholders are not real references
PLACEHOLDER_RE = re.compile(r"YYYY|MM-DD|<[^>]+>|\bXX\b")
INDEX_NAME = "00_INDEX.md"     # the exact required index filename
INDEX_STALE_DAYS = 0           # index older than newest sibling file = stale

# Workstation root may contain ONLY these (plus sub-workstation dirs).
WORKSTATION_ROOT_ALLOWED_FILES = {"CLAUDE.md", "MEMORY.md", ".DS_Store"}

# Root-level items that are infrastructure, not workstations.
NON_WORKSTATION_DIRS = {"00_Resources", "00_System"}
IGNORE_DIRS = {".git", "__pycache__", "node_modules"}
IGNORE_FILES = {".DS_Store", ".gitkeep"}
# Cloud-sync staging files (Google Drive): let the sync tool manage these, never touch.
DRIVE_TMP_RE = re.compile(r"^\.tmp\.drive")

# Unambiguously machine-regenerable cruft (the ONLY auto-removable class,
# and even then this script only reports it).
CRUFT_NAMES = {"__pycache__"}
CRUFT_SUFFIXES = {".pyc", ".pyo"}

DATE_PREFIX_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")
# near-miss date prefixes: unpadded, wrong separator, or trailing space
SLOPPY_DATE_RE = re.compile(r"^\d{4}[-_.]\d{1,2}[-_.]\d{1,2}[-_ ]")
LAST_UPDATED_RE = re.compile(r"last updated[:\s]*(\d{4}-\d{2}-\d{2})", re.I)
LIVING_ROW_RE = re.compile(r"^\|\s*`([^`|]+)`[^|]*\|\s*[^|]*\U0001f7e2", re.M)

findings = []          # (severity, area, message)


def flag(severity, area, message):
    findings.append((severity, area, message))


# ---------------------------------------------------------------- helpers

def find_root(start: Path):
    p = start.resolve()
    for cand in [p, *p.parents]:
        if (cand / "CLAUDE.md").is_file() and (cand / "00_System").is_dir():
            return cand
    return None


def is_workstation(d: Path):
    return (d / "CLAUDE.md").is_file() and (d / "MEMORY.md").is_file()


def resources_dir(ws: Path):
    """A workstation's Resources folder is '[Name] Resources' by convention."""
    cand = ws / f"{ws.name} Resources"
    if cand.is_dir():
        return cand
    # fall back: any dir ending in ' Resources'
    for c in ws.iterdir():
        if c.is_dir() and c.name.endswith(" Resources"):
            return c
    return None


def newest_mtime(folder: Path):
    newest = 0
    for r, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in files:
            if f in IGNORE_FILES or f == INDEX_NAME:
                continue
            try:
                newest = max(newest, (Path(r) / f).stat().st_mtime)
            except OSError:
                pass
    return newest


def visible_children(d: Path):
    out = []
    for c in sorted(d.iterdir()):
        if (c.name in IGNORE_FILES or DRIVE_TMP_RE.match(c.name)
                or c.name.startswith(".")):
            continue          # hidden entries (.claude/, .codex/, .git/) aren't content
        out.append(c)
    return out


# ---------------------------------------------------------------- checks

def check_memory_caps(root: Path):
    for mem in root.rglob("MEMORY.md"):
        n = sum(1 for _ in mem.open(encoding="utf-8", errors="replace"))
        if n > MEMORY_LINE_CAP:
            flag("WARN", rel(root, mem),
                 f"MEMORY.md is {n} lines (cap {MEMORY_LINE_CAP}) — run the "
                 f"memory-maintenance skill: compress verbose entries, then "
                 f"archive completed items to ARCHIVE.md.")


def check_index(root: Path, folder: Path, label: str):
    """Folder is required to carry a current 00_INDEX.md."""
    idx = folder / INDEX_NAME
    if not idx.is_file():
        flag("WARN", label, f"Missing {INDEX_NAME}.")
        return
    text = idx.read_text(encoding="utf-8", errors="replace")
    m = LAST_UPDATED_RE.search(text)
    if not m:
        flag("INFO", label, f"{INDEX_NAME} has no 'Last updated:' line.")
    else:
        idx_date = m.group(1)
        newest = newest_mtime(folder)
        if newest:
            newest_day = datetime.fromtimestamp(newest, LOCAL_TZ).date().isoformat()
            if newest_day > idx_date:
                flag("WARN", label,
                     f"{INDEX_NAME} last updated {idx_date}, but files in the "
                     f"folder were modified as recently as {newest_day} — "
                     f"index may be stale.")
    # living docs (rows marked green in the index) must carry a
    # "Last updated:" line — that's the naming convention for living docs.
    for m in LIVING_ROW_RE.finditer(text):
        tok = m.group(1).strip().rstrip("/")
        if not tok.endswith(".md") or "…" in tok or ".." in tok:
            continue
        target = None
        for base in (folder, folder.parent):
            if (base / tok).is_file():
                target = base / tok
                break
        if target is None or target.name == INDEX_NAME:
            continue
        body = target.read_text(encoding="utf-8", errors="replace")
        if not re.search(r"last updated", body[:2000], re.I):
            flag("INFO", label,
                 f"Living doc `{tok}` (marked \U0001f7e2 in the index) has "
                 f"no 'Last updated:' line near the top — add one per the "
                 f"naming convention.")

    # unindexed items: direct children not mentioned anywhere in the index.
    # A child counts as mentioned if its full name OR its stem (name minus
    # extension) appears — indexes legitimately use collective entries like
    # "`Resume.md` (+ `.docx`, `.pdf`)" or extensionless mentions.
    def mentioned(name):
        return name in text or Path(name).stem in text
    missing = [c.name for c in visible_children(folder)
               if c.name != INDEX_NAME and not mentioned(c.name)]
    if missing:
        listed = ", ".join(f"'{n}'" for n in missing[:10])
        more = f" (+{len(missing) - 10} more)" if len(missing) > 10 else ""
        flag("INFO", label,
             f"{len(missing)} item(s) not mentioned in {INDEX_NAME}: "
             f"{listed}{more} — add them or confirm they're covered by a "
             f"collective entry.")


def check_workstation(root: Path, ws: Path, parent_label=""):
    label = (parent_label + " → " if parent_label else "") + ws.name
    res = resources_dir(ws)

    for c in visible_children(ws):
        if c.is_file():
            if c.name not in WORKSTATION_ROOT_ALLOWED_FILES:
                flag("WARN", label,
                     f"Loose file at workstation root: '{c.name}' — should "
                     f"live inside the Resources folder (confirm with the owner "
                     f"before moving).")
        elif c.is_dir():
            if res is not None and c == res:
                continue
            if is_workstation(c):
                # nested sub-workstation — recurse
                check_workstation(root, c, label)
            else:
                flag("INFO", label,
                     f"Directory '{c.name}/' at workstation root is neither "
                     f"the Resources folder nor a sub-workstation (no "
                     f"CLAUDE.md+MEMORY.md). May be a deliberate project "
                     f"folder — presumed deliberate; confirm before touching.")

    if res is None:
        flag("WARN", label,
             f"No '[{ws.name}] Resources/' folder found. If this workstation "
             f"is a self-contained project pattern, confirm and note it; "
             f"otherwise scaffold one (new-workstation skill).")
    else:
        check_index(root, res, f"{label} / {res.name}")
        # Resources root: only 00_INDEX.md + one driver doc may sit here
        root_files = [c for c in visible_children(res)
                      if c.is_file() and c.name != INDEX_NAME]
        # Exemption (root AGENTS.md placement rule 3): a deliberate
        # numbered + indexed sequence (e.g. a 00-09 handbook) stays flat.
        numbered = [f for f in root_files
                    if re.match(r"^\d{2}[-_]", f.name)]
        if len(numbered) >= 3 and len(numbered) == len(root_files) \
                and (res / INDEX_NAME).is_file():
            root_files = []
        if len(root_files) > 1:
            names = ", ".join(f"'{f.name}'" for f in root_files)
            flag("INFO", f"{label} / {res.name}",
                 f"{len(root_files)} files at the Resources root ({names}). "
                 f"Convention allows only {INDEX_NAME} + ONE driver doc — if "
                 f"more than one of these is a reference doc, group into "
                 f"typed subfolders. (Deliberate numbered handbooks are "
                 f"exempt — check before moving.)")


def check_cruft(root: Path):
    for r, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d != ".git"]
        for d in list(dirs):
            if d in CRUFT_NAMES:
                flag("INFO", rel(root, Path(r) / d),
                     "Machine-regenerable build artifact (safe to remove per "
                     "root AGENTS.md rule 6, but still show the owner first).")
        for f in files:
            if Path(f).suffix in CRUFT_SUFFIXES:
                flag("INFO", rel(root, Path(r) / f),
                     "Compiled Python artifact (regenerable).")


def check_date_prefixes(root: Path):
    """Files that look date-prefixed but have malformed/invalid dates."""
    from datetime import datetime as _dt
    for r, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in files:
            if f in IGNORE_FILES:
                continue
            if DATE_PREFIX_RE.match(f):
                try:
                    _dt.strptime(f[:10], "%Y-%m-%d")
                except ValueError:
                    flag("WARN", rel(root, Path(r) / f),
                         f"Date prefix '{f[:10]}' is not a valid calendar "
                         f"date — rename (with the owner's confirmation).")
            elif SLOPPY_DATE_RE.match(f):
                flag("INFO", rel(root, Path(r) / f),
                     "Looks date-prefixed but doesn't match the strict "
                     "YYYY-MM-DD- convention (padding/separator) — consider "
                     "renaming (with the owner's confirmation).")


def check_md_references(root: Path):
    """Backticked relative paths in CLAUDE.md / MEMORY.md / 00_INDEX.md
    files that don't resolve.

    Bare filenames (no slash) are searched anywhere under the owning
    workstation's subtree — these files legitimately name docs that live
    deeper in Resources. Slashed paths are resolved from the workstation
    root, the Resources folder, the file's own folder, and the workspace
    root. Only unresolvable tokens flag.
    """
    sources = [p for p in (list(root.rglob("CLAUDE.md"))
                           + list(root.rglob("MEMORY.md"))
                           + list(root.rglob(INDEX_NAME)))
               if "_archive" not in p.parts]
    # Living reference docs (ROADMAP item #2, added 2026-07-16): any .md with
    # a "Last updated:" line near the top is a living doc whose backticked
    # path references should also resolve. Skip AUTO-GENERATED files (their
    # rows regenerate), date-prefixed artifacts (point-in-time snapshots may
    # legitimately reference since-moved paths), and 00_System/Skills/
    # (SKILL.md files cite convention-pattern paths as examples by design).
    skills_dir = root / "00_System" / "Skills"
    # Names under the Skills library and under the whole workspace, so that
    # docs citing a skill's scripts (`scripts/score.py`, `SKILL.md`) and
    # infrastructure indexes citing workspace files resolve (2026-09-27).
    skill_names = set()
    workspace_names = set()
    for r, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        workspace_names.update(files)
        workspace_names.update(dirs)
        if skills_dir in Path(r).parents or Path(r) == skills_dir:
            skill_names.update(files)
            skill_names.update(dirs)
    for r, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS
                   and d not in {"_archive", "_superseded"}]
        if Path(r) == skills_dir.parent and skills_dir.is_dir():
            dirs[:] = [d for d in dirs if d != "Skills"]
        for f in files:
            if (not f.endswith(".md")
                    or f in {INDEX_NAME, "CLAUDE.md", "MEMORY.md"}
                    or DATE_PREFIX_RE.match(f)):
                continue
            fp = Path(r) / f
            try:
                head = fp.read_text(encoding="utf-8", errors="replace")[:2000]
            except OSError:
                continue
            if "AUTO-GENERATED" in head:
                continue
            if re.search(r"last updated", head, re.I):
                sources.append(fp)
    for cm in sources:
        # owning workstation = nearest ancestor with CLAUDE.md (or the file's
        # own folder for infrastructure indexes)
        ws = cm.parent
        for anc in [cm.parent, *cm.parent.parents]:
            if anc == root:
                break
            if (anc / "CLAUDE.md").is_file():
                ws = anc
                break
        res = resources_dir(ws)
        text = cm.read_text(encoding="utf-8", errors="replace")
        seen = set()
        # names of all files/dirs under this workstation, for bare-name lookup
        subtree_names = set()
        for r, dirs, files in os.walk(ws):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            subtree_names.update(files)
            subtree_names.update(dirs)
        for m in re.finditer(r"`([^`\n]+)`", text):
            token = m.group(1).strip().rstrip("/")
            if token in seen:
                continue
            seen.add(token)
            if PLACEHOLDER_RE.search(token):
                continue
            if (any(ch in token for ch in "*[]{}<>|#…\"$")
                    or " → " in token or ".." in token or " --" in token
                    or "/ " in token
                    or token.startswith(("--", "./", "/", "~"))):
                continue
            has_ext = re.search(r"\.(md|py|pdf|docx|txt|sh|csv|json)$", token)
            if "/" not in token:
                # bare filename: must look like a real filename and be absent
                # from the entire workstation subtree to flag
                if not has_ext or token.startswith(".") or len(Path(token).stem) < 2:
                    continue
                if token in subtree_names or (root / token).exists():
                    continue
                if token in skill_names:
                    continue
                if ws.name in NON_WORKSTATION_DIRS and token in workspace_names:
                    continue
                flag("INFO", rel(root, cm),
                     f"Reference `{token}` not found anywhere under this "
                     f"workstation — possible dangling path.")
            else:
                # slashed paths: only check when the final component has a
                # recognizable doc extension — dir shorthands ("Evidence/G3"),
                # inside-archive paths (word/footer1.xml), and range notations
                # are prose, not checkable references.
                if not re.search(r"\.(md|py|pdf|docx|txt|sh|csv|json)$",
                                 token):
                    continue
                bases = [ws, root, cm.parent] + ([res] if res else [])
                if skills_dir.is_dir():
                    bases += [d for d in skills_dir.iterdir() if d.is_dir()]
                if any((b / token).exists() for b in bases):
                    continue
                # also try the path's last component as a bare-name fallback
                if Path(token).name in subtree_names:
                    continue
                flag("INFO", rel(root, cm),
                     f"Reference `{token}` doesn't resolve from this "
                     f"workstation, its Resources folder, or the root — "
                     f"possible dangling path.")


# ------------------------------------------------ budgets (added 2026-09-27)

def words(text):
    return len(text.split())


def section(text, heading):
    """Body of a '## <heading>' section (up to the next '## '), or ''."""
    m = re.search(r"^## " + re.escape(heading) + r".*?\n(.*?)(?=^## |\Z)",
                  text, re.S | re.M)
    return m.group(1) if m else ""


def load_overrides():
    """{(workstation, 'status_words'|'memory_words'): budget} from
    budget-overrides.txt next to this skill. Workstation = the folder path
    relative to the workspace root, e.g. 'Job Search' or
    'Creative Projects/Photography'."""
    out = {}
    f = Path(__file__).parent.parent / "budget-overrides.txt"
    if f.is_file():
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [x.strip() for x in line.split("|")]
            if len(parts) >= 3 and parts[1] in {"status_words", "memory_words"} and parts[2].isdigit():
                out[(parts[0], parts[1])] = int(parts[2])
    return out


def check_memory_budgets(root: Path):
    overrides = load_overrides()
    for mem in sorted(root.rglob("MEMORY.md")):
        text = mem.read_text(encoding="utf-8", errors="replace")
        area = rel(root, mem)
        ws = rel(root, mem.parent) if mem.parent != root else "root"
        mem_budget = overrides.get((ws, "memory_words"), MEMORY_WORD_BUDGET)
        status_budget = overrides.get((ws, "status_words"), STATUS_WORD_BUDGET)
        n = words(text)
        if n > mem_budget:
            flag("WARN", area,
                 f"MEMORY.md is {n:,} words (budget {mem_budget:,}). "
                 f"Move dated narrative verbatim to the workstation's "
                 f"Progress Log and keep one-line facts with pointers "
                 f"(memory-maintenance skill).")
        status = section(text, "Current Status")
        sw = words(status)
        if sw > status_budget:
            flag("WARN", area,
                 f"Current Status is {sw:,} words (budget "
                 f"{status_budget}): State, Blocker, Next action, As of. "
                 f"Detail belongs in the Progress Log or STATE.md.")
        long_lines = [len(l.split()) for l in text.splitlines()
                      if len(l.split()) > LINE_WORD_CAP]
        if long_lines:
            flag("INFO", area,
                 f"{len(long_lines)} line(s) over {LINE_WORD_CAP} words "
                 f"(longest {max(long_lines)}). The 150-line cap can't see "
                 f"these; split or move them.")


def root_rules_file(root: Path):
    """The root instructions file: AGENTS.md when present (the Starter Kit
    keeps its root rules there so Claude and ChatGPT/Codex share one file;
    the root AGENTS.md only imports it), otherwise CLAUDE.md."""
    agents = root / "AGENTS.md"
    return agents if agents.is_file() else root / "CLAUDE.md"


def check_claude_sizes(root: Path):
    rootfile = root_rules_file(root)
    if rootfile.is_file():
        b = rootfile.stat().st_size
        if b > ROOT_CLAUDE_BYTES:
            flag("WARN", rootfile.name,
                 f"Root {rootfile.name} is {b / 1024:.1f} KB (budget "
                 f"{ROOT_CLAUDE_BYTES // 1024} KB) and loads into every "
                 f"session. Move procedures into skills or "
                 f"00_System reference docs.")
    for cm in sorted(root.rglob("CLAUDE.md")):
        if cm.parent == root or "00_System" in cm.parts:
            continue
        b = cm.stat().st_size
        if b > WS_CLAUDE_BYTES:
            flag("INFO", rel(root, cm),
                 f"Workstation CLAUDE.md is {b / 1024:.1f} KB (budget "
                 f"{WS_CLAUDE_BYTES // 1024} KB).")


def check_state_files(root: Path):
    for st in sorted(root.rglob("STATE.md")):
        n = sum(1 for _ in st.open(encoding="utf-8", errors="replace"))
        if n > STATE_LINE_CAP:
            flag("INFO", rel(root, st),
                 f"STATE.md is {n} lines (budget {STATE_LINE_CAP}). It is the "
                 f"live dashboard; history belongs in the evidence layer.")


def check_tasks(root: Path):
    tasks = root / "TASKS.md"
    if not tasks.is_file():
        return
    active = section(tasks.read_text(encoding="utf-8", errors="replace"),
                     "Active")
    items = [l.strip() for l in active.splitlines()
             if re.match(r"\s*- \[[ xX]\]", l)]
    open_items = [l for l in items if l.startswith("- [ ]")]
    done_items = [l for l in items if not l.startswith("- [ ]")]
    if len(open_items) > TASK_ACTIVE_CAP:
        flag("WARN", "TASKS.md",
             f"{len(open_items)} open items in Active (budget "
             f"{TASK_ACTIVE_CAP}). Domain task lists belong in their "
             f"workstation; TASKS.md keeps one pointer line per domain.")
    long_items = [l for l in open_items if words(l) - 3 > TASK_WORD_CAP]
    if long_items:
        flag("INFO", "TASKS.md",
             f"{len(long_items)} Active item(s) over {TASK_WORD_CAP} words "
             f"(longest {max(words(l) - 3 for l in long_items)}). Tasks are "
             f"one-liners with a pointer; the detail lives in the workstation.")
    if done_items:
        flag("INFO", "TASKS.md",
             f"{len(done_items)} checked item(s) still under Active; move "
             f"them to Done.")


def check_collisions(root: Path):
    """'name (1).ext' files/folders: Drive or macOS download collisions.
    WARN when the un-suffixed original is missing (references to the
    canonical name dangle), INFO when both exist (a duplicate)."""
    for r, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS
                   and not DRIVE_TMP_RE.match(d)]
        for name in list(dirs) + files:
            m = COLLISION_RE.match(name)
            if not m:
                continue
            original = m.group("stem") + (m.group("ext") or "")
            here = Path(r)
            if (here / original).exists():
                flag("INFO", rel(root, here / name),
                     f"Looks like a sync/download duplicate of "
                     f"'{original}', which also exists. Compare before "
                     f"keeping either (the owner confirms).")
            else:
                flag("WARN", rel(root, here / name),
                     f"Collision-style name and no '{original}' beside it, "
                     f"so references to the canonical name dangle. Rename "
                     f"back with mv -n (the owner confirms).")


def dir_size(d: Path):
    total = 0
    for r, dirs, files in os.walk(d):
        for f in files:
            try:
                total += (Path(r) / f).stat().st_size
            except OSError:
                pass
    return total


def check_heavy_dirs(root: Path):
    """Large '_'-prefixed or build/cache/ocr folders: candidates to keep out
    of the synced tree. Report-only; these are presumed deliberate."""
    for r, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS
                   and not DRIVE_TMP_RE.match(d)]
        for d in list(dirs):
            low = d.lower()
            if d.startswith("_") or low in HEAVY_DIR_NAMES:
                size = dir_size(Path(r) / d)
                if size > HEAVY_DIR_MB * 1024 * 1024:
                    flag("INFO", rel(root, Path(r) / d),
                         f"{size / 1048576:.0f} MB in a build/cache/'_' "
                         f"folder. Presumed deliberate; decide whether it "
                         f"belongs in a cloud-synced workspace.")
                    dirs.remove(d)   # don't re-report its children


def rel(root: Path, p: Path):
    try:
        return str(p.relative_to(root))
    except ValueError:
        return str(p)


# ---------------------------------------------------------------- routing
# Check 13 (2026-09-28). scaffold.py prints the Routing Map row to add, but
# nothing verified it was added, so a workstation without a row stayed
# invisible to sessions. Report-only, like every other check.

ROUTE_SEP = "→"   # the arrow in "Parent → Area" rows
ROOT_ROUTING_HEADING = re.compile(r"^Routing Map\b", re.I)
SUB_ROUTING_HEADING = re.compile(r"^(Sub-Routing Map|Sub-Areas)\b", re.I)


def table_first_cells(text):
    """First cell of every table body row in `text` (header rows dropped)."""
    lines = [l.strip() for l in text.splitlines()]

    def is_sep(l):
        body = l.replace("|", "").strip()
        return l.startswith("|") and "-" in body and set(body) <= set("-: ")

    cells = []
    for i, s in enumerate(lines):
        if not s.startswith("|") or is_sep(s):
            continue
        if i + 1 < len(lines) and is_sep(lines[i + 1]):
            continue                      # header row
        first = s.strip("|").split("|")[0]
        first = first.replace("**", "").replace("`", "").strip()
        if first:
            cells.append(first)
    return cells


def section_cells(claude_md: Path, heading_re):
    """First cells of the table rows under every '## ' section of a
    CLAUDE.md whose heading matches heading_re."""
    if not claude_md.is_file():
        return []
    text = claude_md.read_text(encoding="utf-8", errors="replace")
    cells = []
    for m in re.finditer(r"^## (.+?)\n(.*?)(?=^## |\Z)", text, re.S | re.M):
        if heading_re.search(m.group(1).strip()):
            cells.extend(table_first_cells(m.group(2)))
    return cells


def all_workstations(root: Path):
    """[(segments, path)] for every workstation, sub-workstations included."""
    out = []

    def walk(d: Path, segs):
        for c in visible_children(d):
            if (not c.is_dir() or c.name in NON_WORKSTATION_DIRS
                    or c.name.endswith(" Resources")):
                continue
            if is_workstation(c):
                out.append((segs + [c.name], c))
                walk(c, segs + [c.name])

    walk(root, [])
    return out


def check_routing(root: Path):
    root_rows = [[p.strip() for p in cell.split(ROUTE_SEP)]
                 for cell in section_cells(root_rules_file(root),
                                           ROOT_ROUTING_HEADING)]
    workstations = all_workstations(root)
    # every workstation has a row
    for segs, ws in workstations:
        if segs in root_rows:
            continue
        if len(segs) == 1 and any(r[0] == segs[0] for r in root_rows):
            continue          # a nested parent routes through its areas' rows
        if len(segs) > 1 and segs[-1] in section_cells(
                ws.parent / "CLAUDE.md", SUB_ROUTING_HEADING):
            continue
        flag("WARN", " → ".join(segs),
             "No routing row, so sessions won't load this workstation. Add "
             "one to the root AGENTS.md Routing Map (as 'Parent → Area' "
             "for a sub-workstation) or to the parent's Sub-Routing Map; "
             "draft the route condition with the owner (new-workstation skill, "
             "step 3).")
    # every row points at a workstation
    for r in root_rows:
        if not is_workstation(root.joinpath(*r)):
            flag("WARN", "root AGENTS.md / Routing Map",
                 f"Row '{' → '.join(r)}' points at no workstation "
                 f"('{'/'.join(r)}' has no CLAUDE.md + MEMORY.md). Fix the "
                 f"row after a rename, or confirm with the owner and remove it.")
    for segs, ws in workstations:
        for name in section_cells(ws / "CLAUDE.md", SUB_ROUTING_HEADING):
            if not is_workstation(ws / name):
                flag("WARN", " → ".join(segs),
                     f"Sub-routing row '{name}' points at no sub-workstation "
                     f"('{name}/' has no CLAUDE.md + MEMORY.md). Fix the row "
                     f"after a rename, or confirm with the owner and remove it.")


# ---------------------------------------------------------------- main

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    warn_only = "--warn-only" in sys.argv
    if args:
        root = Path(args[0]).resolve()
    else:
        root = find_root(Path(__file__).parent)
    if not root or not (root / "CLAUDE.md").is_file():
        print("ERROR: couldn't locate workspace root (dir with CLAUDE.md + "
              "00_System/). Pass it explicitly: python3 audit.py <path>")
        return 2

    # 1. memory caps everywhere, then the size budgets (2026-09-27)
    check_memory_caps(root)
    check_memory_budgets(root)
    check_claude_sizes(root)
    check_state_files(root)
    check_tasks(root)

    # 2. each top-level workstation
    for c in visible_children(root):
        if not c.is_dir() or c.name in NON_WORKSTATION_DIRS:
            continue
        if is_workstation(c):
            check_workstation(root, c)
        else:
            flag("INFO", c.name,
                 f"Top-level directory without CLAUDE.md+MEMORY.md — not a "
                 f"workstation. Confirm it's deliberate.")

    # 2b. every workstation has a routing row, every row resolves (2026-09-28)
    check_routing(root)

    # 3. infrastructure folders carry indexes too
    for name in sorted(NON_WORKSTATION_DIRS):
        d = root / name
        if d.is_dir():
            check_index(root, d, name)

    # 4. cruft + naming + dangling references
    check_cruft(root)
    check_date_prefixes(root)
    check_md_references(root)
    check_collisions(root)
    check_heavy_dirs(root)

    # 5. suppress findings the owner has confirmed as deliberate. Each non-empty,
    # non-comment line of accepted-findings.txt is a case-sensitive substring
    # matched against the formatted "[area] message" finding line.
    accepted_file = Path(__file__).parent.parent / "accepted-findings.txt"
    patterns = []
    if accepted_file.is_file():
        for line in accepted_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.append(line)
    kept, suppressed = [], 0
    for sev, area, msg in findings:
        line = f"[{area}] {msg}"
        if any(pat in line for pat in patterns):
            suppressed += 1
        else:
            kept.append((sev, area, msg))
    findings[:] = kept

    # ------------------------------------------------------------ report
    today = datetime.now(LOCAL_TZ).date().isoformat()
    print(f"# Workspace Audit — {today}")
    print(f"Root: {root}")
    print("Report-only. Nothing was modified. Per the owner's rules, show them any")
    print("proposed move/delete/rename and wait for confirmation.\n")
    if suppressed:
        print(f"({suppressed} finding(s) suppressed as owner-confirmed "
              f"deliberate — see accepted-findings.txt)\n")
    if not findings:
        print("CLEAN — no findings. All conventions hold.")
        return 0
    for sev in ("WARN", "INFO"):
        group = [f for f in findings if f[0] == sev]
        if not group:
            continue
        if warn_only and sev == "INFO":
            print(f"({len(group)} INFO finding(s) not shown; run without "
                  f"--warn-only to see them.)\n")
            continue
        print(f"## {sev} ({len(group)})")
        for _, area, msg in group:
            print(f"- [{area}] {msg}")
        print()
    print(f"Total: {len(findings)} finding(s).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
