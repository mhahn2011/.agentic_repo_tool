"""Deterministic grader for map-and-move tasks (C1.12). Runs OUTSIDE the agent.

grade(worktree, task_dir) -> {"pass": bool, "detail": {...}}
Checks: expected layout, no lost files, import-all clean, tests pass at the pinned baseline count.
CLI: python grade.py <task_id> <worktree>   (prints JSON, exit 0 if pass)
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run(cmd, cwd, timeout, env=None):
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=timeout, env=env)
        return p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        return -1, "timeout"
    except OSError as exc:
        return -2, str(exc)


def venv_python(fixture: str) -> str:
    return str(ROOT / "fixtures" / ".venvs" / fixture / "Scripts" / "python.exe")


def load_pins():
    return json.loads((ROOT / "fixtures" / "pins.json").read_text(encoding="utf-8"))


def grade(worktree, task_dir, test_timeout=600) -> dict:
    worktree, task_dir = Path(worktree), Path(task_dir)
    exp = json.loads((task_dir / "expected.json").read_text(encoding="utf-8"))
    pin = load_pins()[exp["fixture"]]
    detail = {}

    # 1. expected layout
    missing = [p for p in exp["must_exist"] if not (worktree / p).is_file()]
    lingering = [p for p in exp["must_not_exist"] if (worktree / p).exists()]
    detail["layout"] = {"ok": not missing and not lingering, "missing": missing, "lingering": lingering}

    # 2. no lost files: every pinned .py file except the moved ones still exists
    rc, out = _run(["git", "ls-tree", "-r", "--name-only", pin["commit"]], worktree, 60)
    pinned = [f for f in out.splitlines() if f.endswith(".py")] if rc == 0 else []
    froms = {m["from"] for m in exp["moves"]}
    lost = [f for f in pinned if f not in froms and not (worktree / f).is_file()]
    detail["no_lost_files"] = {"ok": rc == 0 and bool(pinned) and not lost, "lost": lost[:20]}

    env = dict(os.environ, PYTHONPATH=str(worktree), PYTHONDONTWRITEBYTECODE="1")
    py = venv_python(exp["fixture"])

    # 3. import-all
    rc, out = _run([py, str(ROOT / "fixtures" / "import_all.py"), str(worktree)] + pin["import_packages"],
                   worktree, 300, env)
    try:
        rep = json.loads(out.strip().splitlines()[-1])
        detail["imports"] = {"ok": not rep["broken"], "modules": rep["modules"], "broken": rep["broken"][:10]}
    except (ValueError, IndexError):
        detail["imports"] = {"ok": False, "error": out[-300:]}

    # 4. tests at baseline count
    base = pin["baseline_tests"]["passed"]
    rc, out = _run([py] + pin["test_cmd"], worktree, test_timeout, env)
    m = re.search(r"(\d+) passed", out)
    passed = int(m.group(1)) if m else 0
    bad = re.search(r"(\d+) (failed|error)", out)
    detail["tests"] = {"ok": passed == base and not bad and rc == 0, "passed": passed, "baseline": base,
                       "tail": out.strip().splitlines()[-1][:200] if out.strip() else ""}

    ok = all(v.get("ok") for v in detail.values())
    return {"pass": ok, "detail": detail}


def main(argv):
    task_dir = ROOT / "tasks" / argv[1]
    res = grade(argv[2], task_dir)
    print(json.dumps(res, indent=2))
    return 0 if res["pass"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
