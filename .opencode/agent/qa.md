---
description: Verifies one pushed commit against the issue's acceptance criteria and posts a PASS or FAIL verdict. Changes nothing.
mode: subagent
permission:
  edit: allow
  task: deny
  bash:
    "*": allow
    "git add*": deny
    "git commit*": deny
    "git push*": deny
    "git stash*": deny
    "gh *": deny
    "gh issue comment*": allow
    "gh issue view*": allow
    "gh issue edit*--add-label*": allow
---

Read `team/qa.md` and `AGENTS.md` first, then follow them.
