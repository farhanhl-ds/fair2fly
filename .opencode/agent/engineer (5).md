---
description: Implements one groomed issue in its own worktree and branch, with tests.
mode: subagent
permission:
  edit: allow
  task: deny
  bash:
    "*": allow
    "git push*main*": deny
    "gh *": deny
    "gh issue comment*": allow
    "gh issue view*": allow
    "gh issue edit*--add-label*": allow
    "gh issue edit*--remove-label*": allow
---

Read `team/engineer.md` and `AGENTS.md` first, then follow them.
