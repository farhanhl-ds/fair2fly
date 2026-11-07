---
description: Updates affected docs after QA PASS, in the task's worktree and branch.
mode: subagent
permission:
  edit:
    "*": deny
    "docs/**": allow
    "AGENTS.md": allow
    "README.md": allow
  task: deny
  bash:
    "*": deny
    "git status*": allow
    "git diff*": allow
    "git log*": allow
    "git add*": allow
    "git commit*": allow
    "git push*": allow
    "git push*main*": deny
    "gh issue view*": allow
    "gh issue comment*": allow
---

Read `team/documentation.md` and `AGENTS.md` first, then follow them.
