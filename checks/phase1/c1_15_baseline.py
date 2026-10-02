"""C1.15 Baseline health: baseline_tests recorded per fixture, import-all reports 0 broken.
A fixture may instead record baseline_tests.not_runnable_reason. E008_FIXTURES limits the set."""
import json
import os

from common import ROOT, finish, pins, venv_py

from common import sh

try:
    p = pins()
except OSError as exc:
    finish(False, f"pins.json missing: {exc}")
names = os.environ.get("E008_FIXTURES", "arrow,httpie,rich").split(",")
problems = []
for name in names:
    e = p.get(name, {})
    bt = e.get("baseline_tests")
    if not isinstance(bt, dict) or (bt.get("passed") is None and not bt.get("not_runnable_reason")):
        problems.append(f"{name}: baseline_tests missing")
        continue
    py = venv_py(name)
    rc, out = sh([str(py), str(ROOT / "fixtures" / "import_all.py"), str(ROOT / "fixtures" / name)]
                 + e.get("import_packages", []), timeout=300)
    try:
        rep = json.loads(out.strip().splitlines()[-1])
    except (ValueError, IndexError):
        problems.append(f"{name}: import_all gave no JSON: {out[-200:]}")
        continue
    if rep["broken"]:
        problems.append(f"{name}: {len(rep['broken'])} broken imports: {rep['broken'][:3]}")
finish(not problems, "; ".join(problems) or "baselines recorded, 0 broken imports")
