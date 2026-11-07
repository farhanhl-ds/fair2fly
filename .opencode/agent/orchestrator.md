---
description: Runs the fair2fly task loop. Talk to this agent; it launches pm, engineer, qa and documentation.
mode: primary
permission:
  edit: deny
  task:
    "*": deny
    pm: allow
    engineer: allow
    qa: allow
    documentation: allow
  bash:
    "*": deny
    "ls*": allow
    "pgrep*": allow
    "git status*": allow
    "git log*": allow
    "git diff*": allow
    "git fetch*": allow
    "git worktree list*": allow
    "git worktree add*": allow
    "scripts/new-worktree.sh*": allow
    "scripts/check-worktree.sh*": allow
    "gh issue list*": allow
    "gh issue view*": allow
    "gh issue edit*": allow
    "gh issue comment*": allow
    "gh pr create*": allow
    "gh pr view*": allow
    "gh pr list*": allow
    "gh pr checks*": allow
---

Read `team/orchestrator.md` and `AGENTS.md` first, then follow them. Role limits are in `docs/WORKFLOW.md` section 10.
