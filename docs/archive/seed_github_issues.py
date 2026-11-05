#!/usr/bin/env python3
"""One-time seeding of GitHub labels and issues from docs/archive/TASKS.md.

Run from the root of the cloned repository, with `gh` authenticated and the
remote repository already created (empty: no issues, no pull requests).

    python3 seed_github_issues.py            # dry run, prints what it would do
    python3 seed_github_issues.py --apply    # creates labels and issues
    python3 seed_github_issues.py --apply --repo OWNER/NAME

Issues are created in T-xxx order so issue number N equals task T-00N. The
script stops if a number does not match.
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys

TASKS_FILE = "docs/archive/TASKS.md"

LABELS = {
    "phase-1": ("Week 1: foundation", "1d76db"),
    "phase-2": ("Week 2: collection and persistence", "1d76db"),
    "phase-3": ("Week 3: price intelligence", "1d76db"),
    "phase-4": ("Week 4: user-facing application", "1d76db"),
    "phase-5": ("Week 5: notifications and AI", "1d76db"),
    "phase-6": ("Week 6: hardening and release", "1d76db"),
    "decision": ("Tracks a product-owner decision", "5319e7"),
    "scaffold": ("Project and environment setup", "5319e7"),
    "spike": ("Time-boxed exploration; findings are the deliverable", "5319e7"),
    "backend": ("Backend work", "5319e7"),
    "frontend": ("Frontend work", "5319e7"),
    "hardening": ("Testing, security, release, documentation", "5319e7"),
    "proposed": ("Seeded; not yet groomed", "fbca04"),
    "ready": ("Groomed; Definition of Ready satisfied", "0e8a16"),
    "in-progress": ("Branch issue-<n> exists", "0e8a16"),
    "in-qa": ("Implementation report posted; awaiting QA", "0e8a16"),
    "blocked": ("Missing decision or dependency", "b60205"),
    "post-mvp": ("Moved out of a groomed task; not needed for MVP", "c5def5"),
}

TYPE = {1: "scaffold", 2: "scaffold", 3: "spike", 25: "hardening", 26: "hardening",
        27: "hardening", 28: "hardening", 29: "hardening"}
for n in list(range(4, 15)) + [18, 21, 22, 23]:
    TYPE[n] = "backend"
for n in [15, 16, 17, 19, 20, 24]:
    TYPE[n] = "frontend"

PHASES = [(1, 6, "phase-1"), (7, 10, "phase-2"), (11, 14, "phase-3"),
          (15, 20, "phase-4"), (21, 24, "phase-5"), (25, 29, "phase-6")]


def phase_of(n):
    for lo, hi, name in PHASES:
        if lo <= n <= hi:
            return name
    raise ValueError(f"no phase for T-{n:03d}")


def parse_tasks(text):
    pattern = re.compile(r"^- \[ \] \*\*(T-(\d{3})) — (.+?)\*\*[ ]*\n((?:  .*\n?)+)", re.M)
    tasks = []
    for m in pattern.finditer(text):
        tid, num, title, body = m.group(1), int(m.group(2)), m.group(3), m.group(4)
        lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
        tasks.append({"id": tid, "num": num, "title": title, "lines": lines})
    return tasks


def build_body(task):
    desc, rest = task["lines"][0], task["lines"][1:]
    parts = [desc, ""] + [ln + "\n" for ln in rest]
    parts += [
        "---",
        f"Seeded from the initial backlog (`{TASKS_FILE}`). When this task is about to be "
        "worked, groom it into the full packet (`docs/TASK_TEMPLATE.md`, `team/pm.md`).",
    ]
    return "\n".join(parts)


def gh(args, repo, capture=True):
    cmd = ["gh"] + args + (["--repo", repo] if repo else [])
    return subprocess.run(cmd, check=True, text=True, capture_output=capture).stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="create labels and issues (default: dry run)")
    ap.add_argument("--repo", help="OWNER/NAME (default: the repository of the current directory)")
    args = ap.parse_args()

    path = pathlib.Path(TASKS_FILE)
    if not path.exists():
        sys.exit(f"{TASKS_FILE} not found; run from the repository root")
    tasks = parse_tasks(path.read_text(encoding="utf-8"))

    nums = [t["num"] for t in tasks]
    if nums != list(range(1, len(nums) + 1)):
        sys.exit(f"task numbers are not dense and ordered: {nums}")
    missing = [t["id"] for t in tasks if t["num"] not in TYPE]
    if missing:
        sys.exit(f"no type label mapped for: {missing}")
    print(f"parsed {len(tasks)} tasks ({tasks[0]['id']} to {tasks[-1]['id']})")

    if args.apply:
        for kind in ("issue", "pr"):
            existing = json.loads(gh([kind, "list", "--state", "all", "--limit", "1", "--json", "number"], args.repo))
            if existing:
                sys.exit(f"repository already has {kind}s; numbering would not match T-xxx. Aborting.")
        for name, (desc, color) in LABELS.items():
            gh(["label", "create", name, "--description", desc, "--color", color, "--force"], args.repo)
        print(f"created {len(LABELS)} labels")

    for t in tasks:
        title = f"{t['id']}: {t['title']}"
        labels = [phase_of(t["num"]), TYPE[t["num"]], "proposed"]
        if not args.apply:
            print(f"[dry run] {title}  labels={','.join(labels)}")
            continue
        out = gh(["issue", "create", "--title", title, "--body", build_body(t),
                  "--label", ",".join(labels)], args.repo)
        number = int(out.rstrip("/").split("/")[-1])
        print(f"created #{number}: {title}")
        if number != t["num"]:
            sys.exit(f"issue number {number} does not match {t['id']}. Stopped; fix before continuing.")


if __name__ == "__main__":
    main()
