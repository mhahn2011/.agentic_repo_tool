"""C1.12: validate the grader on every task of a suite.
For each task: (a) untouched pinned fixture must FAIL, (b) the reference solution must PASS.
Reference = reference/apply.py if present (hand-written), else map-and-move with reference/plan.json.
Usage: python validate_grader.py <suite> [--only <task-id>] [--map-and-move-only]
Prints a table; exit 0 only if every task validates. With --map-and-move-only it always uses map-and-move
(used to discover which tasks need a manual reference) and always exits 0.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import grade as grader  # noqa: E402
import run_trial as rt  # noqa: E402

TOOL = ROOT / ".agentic_repo_tools/01_project_agnostic_system/01_composable_elements/01_tools/script_map_and_move/cli/refactor_tool.py"


def apply_reference(task_dir: Path, wt: Path, force_tool: bool):
    ref = task_dir / "reference"
    if (ref / "apply.py").exists() and not force_tool:
        cmd, kind = [sys.executable, str(ref / "apply.py")], "manual"
    else:
        cmd, kind = [sys.executable, str(TOOL), "--plan", str(ref / "plan.json"), "--root", str(wt), "--yes",
                     "--no-commit"], "map-and-move"
    p = subprocess.run(cmd, cwd=wt, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
    return kind, p.returncode, p.stdout + p.stderr


def main(argv):
    suite = argv[1]
    only = argv[argv.index("--only") + 1] if "--only" in argv else None
    force_tool = "--map-and-move-only" in argv
    rows, ok_all = [], True
    for task_dir in sorted((ROOT / "tasks" / suite).glob("[0-9]*")):
        if only and task_dir.name != only:
            continue
        exp = json.loads((task_dir / "expected.json").read_text(encoding="utf-8"))
        commit = grader.load_pins()[exp["fixture"]]["commit"]
        # (a) untouched
        wt = rt.make_worktree(exp["fixture"], commit)
        try:
            untouched = grader.grade(wt, task_dir)
        finally:
            rt.remove_worktree(exp["fixture"], wt)
        # (b) reference
        wt = rt.make_worktree(exp["fixture"], commit)
        try:
            kind, rc, out = apply_reference(task_dir, wt, force_tool)
            ref = grader.grade(wt, task_dir)
        finally:
            rt.remove_worktree(exp["fixture"], wt)
        good = (not untouched["pass"]) and ref["pass"]
        ok_all &= good
        why = ""
        if not ref["pass"]:
            d = ref["detail"]
            why = "; ".join(f"{k}: {json.dumps({x: y for x, y in v.items() if x != 'ok'})[:160]}"
                            for k, v in d.items() if not v.get("ok"))
        rows.append(f"{task_dir.name:36} untouched={'FAIL(ok)' if not untouched['pass'] else 'PASS(BAD)'} "
                    f"reference[{kind}]={'PASS' if ref['pass'] else 'FAIL'} {'OK' if good else 'INVALID'} {why}")
    print("\n".join(rows))
    print(f"validated {sum(1 for r in rows if ' OK' in r)}/{len(rows)}")
    return 0 if (ok_all or force_tool) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
