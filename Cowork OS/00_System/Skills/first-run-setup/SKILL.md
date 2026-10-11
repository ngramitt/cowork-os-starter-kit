---
name: first-run-setup
description: Sets up a fresh Cowork OS folder for its owner in about ten minutes. Three short rounds of questions, then it writes their profile, voice and preferences, creates their first workstations, and switches itself off. Use when the root AGENTS.md says "Not set up yet", or when the owner says "re-run setup".
---

# First-Run Setup

Last updated: 2026-10-11 (living document; Cowork OS Starter Kit v1.1)

## What this is

The owner just downloaded or unzipped Cowork OS, opened the folder in their AI tool (Claude or ChatGPT/Codex) and said hello. This procedure turns the blank kit into *their* workspace. It runs once. One of its last steps rewrites the **Setup status** section of the root `AGENTS.md`, so it never triggers again.

Keep it to about ten minutes and about six messages from the owner: hello, three rounds of answers, a "looks right," and their answer on the extras. Everything else the system learns later, as they use it.

## Ground rules while you run it

- **Talk like a person, not a form.** Each round is one short message. If your tool has a multiple-choice question feature, use it for the multiple-choice items and ask the free-text items in the same message. Otherwise ask in a short numbered list and accept loose answers.
- **Plain words.** Don't show the owner markdown table rows, file paths or jargon like "nested parent" unless they ask. Say "areas," not "workstations," until they've seen one.
- **Skipping is always fine.** Use a sensible default and say which one you used.
- **Don't delete or overwrite** anything except the kit's own placeholder text listed in the Build step. On a re-run, update what's there instead of starting over.
- **Nothing sensitive.** Don't ask for account numbers, health details or passwords. Only save what the owner said or confirmed.
- **Use the owner's local date** for everything you write. Once you know their timezone: `TZ=<timezone> date +%F`.

## Step 0: Check the environment (quietly)

1. **Can you see this folder?** List `00_System/`. If you can't, you're probably running in a cloud workspace instead of on the owner's computer. This happens in ChatGPT when a task runs in the cloud rather than locally. Stop and tell the owner in plain words: open the folder in local mode (in ChatGPT's desktop app, choose to work locally on your computer), then say hello again.
2. **Can you write here?** Write the `tool =` line in `00_System/workspace-config.txt` now: `claude`, `chatgpt-codex` or `other`. If the write fails, say so and stop.
3. **Is Python available?** Run `python3 --version`. With Python, the maintenance scripts run. Without it, the system still works, and you follow the scripts' by-hand paths. (On a Mac this command can pop up an install dialog; if it does, treat it as "not available" and carry on.) Write `python = yes` or `no` in the config. Mention Python to the owner only at the end, and only if it's missing.
4. **Timezone hint:** `readlink /etc/localtime` often ends in an IANA name like `America/Chicago`. If you get one that isn't UTC, offer it in Round 1. If you only get UTC or an abbreviation, the machine is probably a server, so ask for their city instead.

Then say hello: "I'm going to set up your Cowork OS: about ten minutes, three quick rounds of questions. After that, this folder becomes your workspace. It remembers what matters, keeps each area of your life or work in its own place, and gets more useful the more you use it."

## Round 1: About you

Ask in one message:

1. What should I call you?
2. In a sentence, what do you do? (Work, school, whatever's most of your week.)
3. What city are you in? (For dates and times. Offer the detected timezone if Step 0 found a real one.) Convert the answer to an IANA name yourself.
4. **Only if your tool actually has memory of this person** (saved memories or past chats you can search): "I may already know a few things about you from our past chats. Want me to pull in the basics so you don't have to repeat them?" If they say yes, look. Show what you found and save only what they confirm. If you find nothing, say so in one line and move on. If your tool has no memory, skip this question entirely.

## Round 2: How you like to work

Ask in one message. The first four are multiple choice; let them answer in their own words too.

1. **Answer length:** short and direct / medium / detailed.
2. **Tone:** casual / professional but friendly / formal.
3. **Recommendations:** one clear pick / a few options to choose from.
4. **Big tasks:** ask me clarifying questions first / just start and I'll steer.
5. *(Optional)* Any words or habits in AI writing that bug you? Anything you always want?
6. *(Optional)* Want me to write in your voice later, for emails or posts? Paste one or two short things you've written and I'll learn from them. Skipping is fine.

## Round 3: Where to start

In one message, show the menu from `STARTER-IDEAS.md` (next to this file): names only, grouped. Ask them to:
- pick **two or three** areas they'll actually use this month, or name their own;
- for each pick, add one line: what's going on right now, and what's the next thing to do. "Nothing yet" is fine.

If they pick something broad with several parts (like Creative Projects with Photography), that's a parent with an area under it, and it still counts as **one pick**.

## Confirm

Draft a routing condition for each pick, in their words, naming the specific things that should route there: people, projects, places, tools. Show them as a plain list, not a table, and ask "Look right?":

- **Job Search:** my job search: applications, interview prep, recruiters and offers

Specific beats vague. "Applications, interview prep, recruiters, offers" routes better than "career stuff."

## Build (after "looks right")

Do all of this without asking anything else. Use the local date everywhere.

1. **`00_System/workspace-config.txt`:** fill in `owner`, `timezone` (an IANA name like `America/Chicago`) and `setup_date`. `tool` and `python` are already set.
2. **`00_Resources/profile.md`:** name, what they do, timezone, tools, and anything confirmed in Round 1. Only what they said.
3. **`00_Resources/voice-principles.md`:** tone, length and phrase preferences from Round 2. If they pasted writing samples, describe the patterns you see (sentence length, formality, favorite phrases, sign-offs). Don't store the samples themselves.
4. **Root `AGENTS.md` → Preferences:** replace the placeholder with three to six instructions from Round 2 ("Keep answers short and direct." "Give one clear recommendation." "Ask clarifying questions before starting a big task.").
5. **Create each area** with the new-workstation skill (`00_System/Skills/new-workstation/SKILL.md`):
   - With Python: `python3 -B 00_System/Skills/new-workstation/scripts/scaffold.py "<Name>"`. For a parent with an area, run `scaffold.py "<Parent>" --as-parent` first, then `scaffold.py "<Area>" --parent "<Parent>"`.
   - Without Python: create the same files by hand from the templates in `00_System/CONVENTIONS.md`.
   - Then, in each one:
     - `CLAUDE.md` → **Identity:** two or three sentences, in their words, on what this area is for and what routes here.
     - `CLAUDE.md` → **Workflow:** three or four simple steps for its main job.
     - `MEMORY.md` → **Current Status:** state (as of today) and next action from Round 3.
   - If a pick has a next action, create `<Name> Resources/Tracking/Tasks.md` in the format in `00_System/CONVENTIONS.md`, with that action as the first `- [ ]` item under Active. Add it to the Resources `00_INDEX.md` and bump that index's `Last updated` date.
   - For a parent with an area, fill in the parent's Sub-Routing Map row, and set the parent's Current Status to "Routes to its areas. Next action: none at this level."
6. **Root `AGENTS.md` → Routing Map:** add the confirmed rows: one per top-level area, and `Parent → Area` for areas under a parent. A parent gets no row of its own. Bump the `Last updated` line at the top of `AGENTS.md`.
7. **Root `MEMORY.md` → Core Memory:** replace "Not set up yet." with two or three one-line facts (name, what they do, timezone).
8. **Root `TASKS.md`:** under Active, one plain pointer line per area that has a `Tasks.md`: `- **<Name>:** <Name>/<Name> Resources/Tracking/Tasks.md`. Bump its `Last updated`.
9. **Switch setup off:** replace the whole **Setup status** section of root `AGENTS.md` with the text below, using the `kit_version` from `00_System/workspace-config.txt`:

    ```
    ## Setup status

    Set up on YYYY-MM-DD for <Name>, from Cowork OS Starter Kit v<kit_version>. To run setup again, the owner says "re-run setup" (see `00_System/Skills/first-run-setup/SKILL.md`).
    ```

10. **Changelog:** write `00_System/YYYY-MM-DD-Setup-Changelog.md` listing every file setup created or changed and the choices made. Add it to `00_System/00_INDEX.md` and bump that index's `Last updated` line.
11. **Check last, after every write:**
    - With Python: `python3 -B 00_System/Skills/work-dashboard/scripts/dashboard.py`, then `python3 -B 00_System/Skills/workspace-audit/scripts/audit.py --warn-only`.
    - Without Python: refresh `DASHBOARD.md` by hand (the work-dashboard skill's "Without Python" section) and do the by-hand audit checklist in the workspace-audit skill.

    Fix anything flagged. It should come back clean.

## Report and offer the extras (one message)

In one message:

**What was set up:** three to five short lines covering their areas, each area's next action, and where the plain-English guide lives (`00_System/GUIDE.md`).

**Three optional extras** (say "yes," "no" or "later" to each):

1. **A monthly health check.** Offer this only if Python is available and their tool can run scheduled tasks against this local folder. Claude's desktop app can; in ChatGPT it depends on the plan and on the task running locally.
   - It runs the prompt in `00_System/Skills/workspace-audit/MONTHLY-AUDIT-PROMPT.md` once a month (suggest the first weekday morning of the month) and uses a small amount of their plan's usage each time.
   - Otherwise, suggest they just say "audit the workspace" once a month.
2. **Shortcut skills.** Three small skills they can add to their Claude or ChatGPT account (`00_System/Account-Skill-Routers/README.md`). Offer to walk them through it.
3. **A two-minute tour** of what to say to it.

If Python is missing, add one line at the end: "If you ever want the automatic checks, installing Python 3 turns them on."

## After they answer

Do only what they said yes to:

- **Health check:** set up the scheduled task in their tool with the prompt and this folder attached. If you can't create it yourself, give them the steps.
- **Skills:** follow the README with them, step by step.
- **Tour:** show the "Things to say" table from `00_System/GUIDE.md` and suggest they try "what's on my plate?" now.

Close in one line: keep using this same folder, because every conversation starts from it.

## Re-running setup

When the owner says "re-run setup," run Rounds 1 to 3 again with their current answers as defaults. Update the files instead of replacing them: add new areas, never remove existing ones, and change Preferences only where they changed an answer. Log it in a new dated changelog.

## What NOT to do

- Don't skip the **Setup status** switch-off, or setup will try to run every session.
- Don't create more than three picks during setup. More come naturally later ("start a workstation for...").
- Don't ask for anything sensitive, and don't invent facts about the owner.
- Don't turn on scheduled tasks or install skills without a clear yes.
