# The Cowork OS Guide

Last updated: 2026-09-28 (living document; Cowork OS Starter Kit v1.0)

A plain-English guide for the person who owns this folder. The AI reads its own instructions elsewhere; this one's for you.

## What this is

Cowork OS turns a folder on your computer into a desk your AI assistant works from. It holds:

- **Rules:** how you like things done.
- **Memory:** what's going on right now.
- **A library:** everything for each area of your life or work.

Instead of re-explaining yourself every conversation, you point Claude or ChatGPT at this folder and it picks up where you left off. The more you use it, the more it knows.

It works with **Claude** (the desktop app, or Claude Code) and with **ChatGPT** (the desktop app's Codex or Work mode, or the Codex CLI). You can even switch between them. Both read the same files.

## The pieces

```
Cowork OS/
├── AGENTS.md        the house rules and the map of your workstations (the AI reads this first)
├── CLAUDE.md        a one-line pointer so Claude reads AGENTS.md too
├── MEMORY.md        the few facts that matter everywhere
├── DASHBOARD.md     one line per workstation: where it stands, what's next (generated)
├── TASKS.md         points to each workstation's to-do list
├── ARCHIVE.md       finished things, kept for history
├── 00_Resources/    your profile and your writing voice
├── 00_System/       the machinery: conventions, skills, scripts, this guide
└── <Workstation>/   one folder per area, like "Job Search" or "Home"
    ├── CLAUDE.md    that area's rules (read by every AI tool; the name is just a convention)
    ├── MEMORY.md    that area's current status, contacts and decisions
    └── <Workstation> Resources/   its documents, sorted into subfolders, with an index
```

## How a conversation works

1. The AI reads `AGENTS.md` and `MEMORY.md`. That's a few thousand words, so it's cheap.
2. It matches your request to a workstation using the Routing Map in `AGENTS.md`. The map is written in your own words, like "route here when I'm working on my job search, interviews, recruiters or offers."
3. It reads that workstation's `CLAUDE.md` and `MEMORY.md`, and only then does the work.
4. Before it wraps up, it saves what changed: the status, the decisions, the documents, each in its proper place.

Everything else stays unread until it's needed. That's why it stays fast even when the folder gets big.

## Things to say

| Say... | What happens |
|---|---|
| "What's on my plate?" | The dashboard and task lists, summarized |
| "Remember this: ..." | Saved to the right memory file, and confirmed |
| "Start a workstation for ..." | A new area is created, with a routing row |
| "Let's start a project: ..." | A project gets a home, a definition of done and a next action |
| "Wrap up" or "write a handoff" | Status updated, and notes left for next time or for another AI |
| "Audit the workspace" | A health check: loose files, stale indexes, bloated memory |
| "X is done, archive it" | The memory moves to `ARCHIVE.md`, after you confirm |
| "That doesn't sound like me" | Your voice file gets updated from your edits |
| "Re-run setup" | The setup questions again, with your current answers as defaults |
| "Review the whole system" | A careful, step-by-step tune-up, about once a year |

## Rules it always follows

- **It never deletes anything** without your explicit OK.
- **It shows you moves and renames** before doing them.
- **Statuses stay short** (80 words). History goes to a Progress Log, so nothing is lost and nothing bloats.
- **Moves are word for word.** It never summarizes something and throws away the original.
- **When it's unsure where something goes, it asks.**

## Using it with Claude

- **Claude desktop app:** start a new task and add this folder to it. Claude reads `CLAUDE.md`, which pulls in `AGENTS.md`.
- **Claude Code:** open a terminal in this folder and run `claude`.
- The maintenance scripts run inside Claude's own environment, so there's nothing to install.

## Using it with ChatGPT

- **ChatGPT desktop app:** use **Codex** (or **Work**, if your plan has it) and open this folder. Make sure it's working **locally on your computer**, not in the cloud. If it says it can't see your files, that's the problem. Codex reads `AGENTS.md` automatically. If it ever doesn't, start with "Read AGENTS.md and follow it."
- **Codex CLI:** open a terminal in this folder and run `codex`.
- The maintenance scripts need **Python 3** on your computer. Macs often prompt you to install it the first time. The system works without it; the AI just does the checks by hand.

## FAQ

**Can I edit the files myself?** Yes. They're plain text. Keep statuses short, and the AI will tidy anything else.

**Where does my data go?** The folder stays on your computer. Your AI tool reads the files it needs to answer you, the same as any file you share with it. Don't put passwords or full account numbers in here.

**What should I back up?** The whole folder. A sync service like iCloud, Dropbox or Google Drive is convenient, but sync isn't backup: one bad edit syncs everywhere. Keep an occasional copy somewhere else.

**Why are the workstation rules files called `CLAUDE.md` if I use ChatGPT?** It's just the name the system uses for "this area's rules." The root instructions tell every AI tool to read it, so it works the same in ChatGPT.

**It feels cluttered.** Say "audit the workspace." It will find loose files and stale lists and propose fixes. It won't move anything until you say yes.

**It forgot something.** Say "remember this: ...". If it keeps forgetting the same kind of thing, ask it to add a rule to that workstation's `CLAUDE.md`, or to `AGENTS.md` if it applies everywhere.

**Can I rename a workstation?** Yes. Ask for it, and the AI will show you the move and update every reference and the Routing Map.
