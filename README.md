# Cowork OS Starter Kit

**A folder that turns your AI assistant into a real collaborator.** It remembers what matters, keeps each part of your life or work in its own place, and gets more useful the more you use it. It works with **Claude** or **ChatGPT**.

Instead of re-explaining yourself every conversation, you point your AI at this folder and it picks up where you left off. Setup takes about ten minutes and happens on its own the first time you open it.

## Get started

1. **Download it.** Click the green **Code** button above, then **Download ZIP**.
2. **Unzip it.** Inside is a folder called `Cowork OS`. Move it somewhere permanent, like your Documents folder, and keep the name.
3. **Open it in your AI tool and say hi.**
   - **Claude desktop app:** start a new task and add the `Cowork OS` folder.
   - **ChatGPT desktop app:** use **Codex** (or **Work**), open the folder, and set it to work **locally on your computer**.
   - **Claude Code or Codex CLI:** open a terminal in the folder and run `claude` or `codex`.

Setup starts by itself: three quick rounds of questions about you, how you like to work, and two or three areas to start with. The full instructions are in [`Cowork OS/START-HERE.md`](Cowork%20OS/START-HERE.md).

## What you get

- **Workstations:** one folder per area of your life or work, like "Job Search," "Home" or "Training," each with its own rules and memory.
- **Memory that stays tidy:** short status notes, with history kept in logs so nothing bloats or gets lost.
- **A dashboard:** "What's on my plate?" gets you every area's next step in one view.
- **Health checks:** an optional script spots loose files and stale notes, and never moves or deletes anything without your OK.
- **A plain-English guide:** [`Cowork OS/00_System/GUIDE.md`](Cowork%20OS/00_System/GUIDE.md) covers what to say to it and answers common questions.

## Good to know

- **Your files stay on your computer.** Your AI tool reads only what it needs. Don't store passwords or full account numbers in the folder.
- **Python 3 is optional.** It powers the automatic checks. Claude's desktop app has it built in; everything works without it.
- **Use Download ZIP rather than copying files one by one,** so the folder arrives complete. (Cloning with git works too, but Download ZIP keeps the first health check cleanest.)
- **Already set up?** Keep using your own folder. Don't download over it: your workspace has your answers, areas and memory in it, and a fresh copy would start setup again.

## What's in this repo

| Path | What it is |
|---|---|
| `Cowork OS/` | The kit itself: the folder you move and open in your AI tool |
| `Cowork OS/START-HERE.md` | Setup in three steps |
| `Cowork OS/00_System/GUIDE.md` | The plain-English guide and FAQ |
| `LICENSE` | MIT: use it, change it and share it freely; keep the copyright notice |

## Questions or feedback

Tell the person who sent you this link. Notes on what confused you during setup are especially helpful, since they shape the next version. If you're comfortable with GitHub, you can also open an issue.

## License

MIT. See [`LICENSE`](LICENSE).
