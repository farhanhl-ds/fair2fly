#!/usr/bin/env python3
"""One-time seeding of GitHub labels, milestones, and issues from docs/archive/TASKS.md.

Run from the root of the cloned repository, with `gh` authenticated and the
remote repository already created (empty: no issues, no pull requests).

    python3 seed_github_issues.py            # dry run, prints what it would do
    python3 seed_github_issues.py --apply    # creates labels, milestones, issues
    python3 seed_github_issues.py --apply --repo OWNER/NAME

Milestones are read from the "## Milestone N — Name" headings of TASKS.md, so the
tracker follows the roadmap. Each task goes to the milestone of the section it sits
in. Issues are created in T-xxx order so issue number N equals task T-0NN. The
script stops if a number does not match.
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys

TASKS_FILE = "docs/archive/TASKS.md"

# Label descriptions are what the GitHub label page shows; keep them short.
LABELS = {
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

# Type label per task number. Everything not listed here is a backend task.
TYPE = {1: "scaffold", 2: "scaffold", 3: "spike", 30: "scaffold"}
for n in (25, 26, 27, 28, 29):
    TYPE[n] = "hardening"
for n in (15, 16, 17, 19, 20, 24):
    TYPE[n] = "frontend"
BACKEND = set(range(4, 15)) | {18, 21, 22, 23}


def type_of(n):
    if n in TYPE:
        return TYPE[n]
    if n in BACKEND:
        return "backend"
    return None


def parse_tasks(text):
    """Return (milestones, tasks). Each task carries its milestone title."""
    heading = re.compile(r"^## Milestone (\d+) — (.+?)(?: \(closed\))?\s*$", re.M)
    task = re.compile(r"^- \[ \] \*\*(T-(\d{3})) — (.+?)\*\*[ ]*\n((?:  .*\n?)+)", re.M)
    marks = list(heading.finditer(text))
    milestones, tasks = [], []
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        title = f"Milestone {m.group(1)}: {m.group(2)}"
        found = list(task.finditer(text[m.end():end]))
        if not found:
            continue  # Milestone 0 holds decisions only; it gets no GitHub milestone.
        milestones.append((title, m.group(2)))
        for t in found:
            lines = [ln.strip() for ln in t.group(4).splitlines() if ln.strip()]
            tasks.append({"id": t.group(1), "num": int(t.group(2)), "title": t.group(3),
                          "lines": lines, "milestone": title})
    tasks.sort(key=lambda t: t["num"])
    return milestones, tasks


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


def api(path, repo, extra=()):
    """gh api against the repo; {owner}/{repo} placeholders resolve from the current directory."""
    base = f"repos/{repo}" if repo else "repos/{owner}/{repo}"
    return subprocess.run(["gh", "api", f"{base}/{path}", *extra], check=True, text=True,
                          capture_output=True).stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="create labels, milestones, issues (default: dry run)")
    ap.add_argument("--repo", help="OWNER/NAME (default: the repository of the current directory)")
    args = ap.parse_args()

    path = pathlib.Path(TASKS_FILE)
    if not path.exists():
        sys.exit(f"{TASKS_FILE} not found; run from the repository root")
    milestones, tasks = parse_tasks(path.read_text(encoding="utf-8"))

    nums = [t["num"] for t in tasks]
    if nums != list(range(1, len(nums) + 1)):
        sys.exit(f"task numbers are not dense and ordered: {nums}")
    missing = [t["id"] for t in tasks if type_of(t["num"]) is None]
    if missing:
        sys.exit(f"no type label mapped for: {missing}")
    print(f"parsed {len(tasks)} tasks ({tasks[0]['id']} to {tasks[-1]['id']}) "
          f"in {len(milestones)} milestones")

    if args.apply:
        for kind in ("issue", "pr"):
            existing = json.loads(gh([kind, "list", "--state", "all", "--limit", "1", "--json", "number"], args.repo))
            if existing:
                sys.exit(f"repository already has {kind}s; numbering would not match T-xxx. Aborting.")
        for name, (desc, color) in LABELS.items():
            gh(["label", "create", name, "--description", desc, "--color", color, "--force"], args.repo)
        print(f"created {len(LABELS)} labels")
        have = {m["title"] for m in json.loads(api("milestones?state=all&per_page=100", args.repo))}
        for title, name in milestones:
            if title in have:
                continue
            api("milestones", args.repo, ["-f", f"title={title}",
                                           "-f", f"description=Roadmap section: {name} (docs/ROADMAP.md)"])
        print(f"milestones ready: {len(milestones)}")

    for t in tasks:
        title = f"{t['id']}: {t['title']}"
        labels = [type_of(t["num"]), "proposed"]
        if not args.apply:
            print(f"[dry run] {title}  milestone={t['milestone']!r}  labels={','.join(labels)}")
            continue
        out = gh(["issue", "create", "--title", title, "--body", build_body(t),
                  "--label", ",".join(labels), "--milestone", t["milestone"]], args.repo)
        number = int(out.rstrip("/").split("/")[-1])
        print(f"created #{number}: {title}")
        if number != t["num"]:
            sys.exit(f"issue number {number} does not match {t['id']}. Stopped; fix before continuing.")


if __name__ == "__main__":
    main()
