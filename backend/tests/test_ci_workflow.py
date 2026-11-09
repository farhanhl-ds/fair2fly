"""Guardrails for the CI workflow added by T-030."""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "ci.yml"
README = REPO_ROOT / "README.md"

MAKE_TARGETS = ["make install", "make lint", "make typecheck", "make test"]


def _search(pattern: str, text: str) -> re.Match[str]:
    match = re.search(pattern, text, flags=re.MULTILINE)
    assert match is not None, f"{pattern!r} not found"
    return match


def _run_commands(workflow: str) -> list[str]:
    return re.findall(r"^\s+run:\s*(.+?)\s*$", workflow, flags=re.MULTILINE)


def _uses(workflow: str) -> list[str]:
    return re.findall(r"^\s+uses:\s*(\S+)\s*$", workflow, flags=re.MULTILINE)


def test_ci_runs_documented_make_targets_for_pull_requests_ac_1() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    _search(r"^name:\s*ci$", workflow)
    _search(r"^  ci:$", workflow)
    _search(r"^  pull_request:$", workflow)
    for activity in ("opened", "synchronize", "reopened"):
        assert activity in workflow
    assert _run_commands(workflow) == MAKE_TARGETS


def test_ci_runs_on_every_push_to_main_ac_2() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    _search(r"^  push:\n    branches: \[main\]$", workflow)
    group = _search(r"^  group:\s*(.+)$", workflow).group(1)
    assert "github.event.pull_request.number" in group
    assert "github.sha" in group
    assert "cancel-in-progress: ${{ github.event_name == 'pull_request' }}" in workflow


def test_ci_has_no_check_logic_of_its_own_ac_3() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert _run_commands(workflow) == MAKE_TARGETS
    assert "continue-on-error" not in workflow
    assert "|| true" not in workflow


def test_ci_pins_toolchain_and_actions_and_is_read_only_ac_4() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    _search(r"^    runs-on: ubuntu-24\.04$", workflow)
    _search(r"^permissions:\n  contents: read$", workflow)
    assert 'version: "0.13.7"' in workflow
    assert 'python-version: "3.14"' in workflow
    assert "node-version-file: frontend/.nvmrc" in workflow
    assert "cache-dependency-glob: backend/uv.lock" in workflow
    assert "cache-dependency-path: frontend/package-lock.json" in workflow
    assert "@latest" not in workflow
    assert "secrets." not in workflow
    assert "pull_request_target" not in workflow
    for action in _uses(workflow):
        _, _, ref = action.partition("@")
        assert re.fullmatch(r"v\d+\.\d+\.\d+|[0-9a-f]{40}", ref), action


def test_readme_documents_the_ci_check_ac_5() -> None:
    readme = README.read_text(encoding="utf-8")

    assert "## Continuous integration" in readme
    section = readme.split("## Continuous integration", maxsplit=1)[1]
    assert ".github/workflows/ci.yml" in section
    assert "`ci`" in section
    assert "pull request" in section
    assert "push to `main`" in section
    assert "status check" in section
    assert "product owner" in section
