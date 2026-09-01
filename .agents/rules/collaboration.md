---
name: Team Collaboration Guidelines
description: Rules for Antigravity agents to avoid merge conflicts and coordinate work across multiple collaborators.
---

# Team Collaboration Rules

Since multiple developers (and their Antigravity agents) are working on this repository for a hackathon, you must follow these rules strictly to prevent merge conflicts and ensure smooth collaboration:

## 1. Branching Strategy
- NEVER commit directly to the `main` or `master` branch.
- Always check the current branch using `git branch`. If the user asks you to start a new task and you are on `main`, PROPOSE creating and switching to a new branch (e.g., `git checkout -b feature/component-name`).
- Before starting work, always ensure your local branch is up to date with the remote by running `git pull origin <branch-name>`.

## 2. Scope Containment
- Only modify files that are strictly related to your current task. 
- Do NOT refactor or reformat code in files you are not actively working on, as another agent might be modifying them simultaneously.
- If a change requires modifying a core file (like `app.py` or `schema.sql`), keep the changes as localized and minimal as possible.

## 3. Communication via Code Comments
- If you are implementing a complex feature, leave clear inline comments explaining your logic so other agents (and humans) can easily understand and build upon it later.

## 4. Pull Requests
- When a task is complete, stage and commit the changes with a clear, descriptive commit message.
- Advise the user to push the branch and open a Pull Request (PR) rather than merging locally.

## 5. User Roles & Restrictions
- **Aarlyn, Sahasra, & Akshay**: If the user you are assisting is Aarlyn, Sahasra, or Akshay, you are **ONLY** permitted to modify UI files (e.g., HTML files in `templates/`, CSS/JS in `static/`). If a task requires modifying ANY other file (like `app.py`, backend logic, or database schema), you MUST refuse to make the change and explicitly instruct the user to contact **Lakshith** to perform that modification.
