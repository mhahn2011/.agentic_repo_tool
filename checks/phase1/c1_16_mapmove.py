"""C1.16 map-and-move: dry run changes nothing; one real move leaves 0 broken imports and baseline test count."""
import json
import sys
import tempfile
from pathlib import Path

from common import PY, ROOT, finish, pins, reset_cmd, sh, venv_py

TOOL = (ROOT / ".agentic_repo_tools/01_project_agnostic_system/01_composable_elements/01_tools/"
        "script_map_and_move/cli/refactor_tool.py")
FX = ROOT / "fixtures" / "arrow"
VENV = venv_py("arrow")
RESET = reset_cmd("arrow")
problems = []
if not TOOL.exists():
    finish(False, f"tool not found: {TOOL}")
sh(RESET)
plan = Path(tempfile.mkdtemp()) / "plan.json"
plan.write_text(json.dumps({"moves": [{"from": "arrow/constants.py", "to": "arrow/core/constants.py"}]}), encoding="utf-8")
rc, out = sh([PY, str(TOOL), "--plan", str(plan), "--root", str(FX), "--dry-run", "--yes"])
_, st = sh(["git", "-C", str(FX), "status", "--porcelain"])
if rc != 0 or st.strip():
    problems.append(f"dry run rc={rc}, status={st.strip()[:200]}")
rc, out = sh([PY, str(TOOL), "--plan", str(plan), "--root", str(FX), "--yes", "--no-commit"])
if rc != 0:
    problems.append(f"real move rc={rc}: {out[-300:]}")
p = pins()["arrow"]
rc, out = sh([str(VENV), str(ROOT / "fixtures" / "import_all.py"), str(FX)] + p["import_packages"])
try:
    rep = json.loads(out.strip().splitlines()[-1])
    if rep["broken"]:
        problems.append(f"{len(rep['broken'])} broken imports after move: {rep['broken'][:3]}")
except (ValueError, IndexError):
    problems.append(f"import_all output: {out[-200:]}")
rc, out = sh([str(VENV), "-m", "pytest", "-q", "-p", "no:cacheprovider", "-o", "addopts="], cwd=FX, timeout=300)
summary = out.strip().splitlines()[-1] if out.strip() else ""
sys.path.insert(0, str(ROOT / "runner"))
import grade  # noqa: E402
if f"{grade.baseline_for(p)['passed']} passed" not in summary:
    problems.append(f"test count != baseline: {summary}")
sh(RESET)
finish(not problems, "; ".join(problems) or "dry run clean, real move ok, tests at baseline")
