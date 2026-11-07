---
description: Grooms one GitHub issue into a Ready task packet. Writes no code.
mode: subagent
permission:
  edit: deny
  task: deny
  bash:
    "*": deny
    "git status*": allow
    "git log*": allow
    "gh issue list*": allow
    "gh issue view*": allow
    "gh issue edit*": allow
    "gh issue create*": allow
    "gh issue comment*": allow
---

Read `team/pm.md` and `AGENTS.md` first, then follow them.
