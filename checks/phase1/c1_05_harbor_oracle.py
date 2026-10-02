"""C1.5: Harbor container path. Oracle agent on one Terminal-Bench 2.0 task (regex-log) must score reward 1.0."""
import json
import os
from pathlib import Path
import shutil

from common import ROOT, finish, sh

HARBOR = str(Path.home() / ".local" / "bin" / ("harbor.exe" if os.name == "nt" else "harbor"))
env = dict(os.environ, PYTHONIOENCODING="utf-8")
env.pop("ANTHROPIC_API_KEY", None)
jobs = ROOT / "runs" / "harbor-jobs"
name = "oracle-regex-log-check"
shutil.rmtree(jobs / name, ignore_errors=True)
rc, out = sh([HARBOR, "run", "-d", "terminal-bench@2.0", "-a", "oracle", "-i", "regex-log", "-e", "docker",
              "--job-name", name, "-o", str(jobs), "-y"], timeout=900, env=env)
res = jobs / name / "result.json"
if rc != 0 or not res.exists():
    finish(False, f"harbor rc={rc}: {out.strip()[-300:]}")
ok = "1.000" in out and "Exceptions" in out
finish(ok, "oracle reward 1.0 on terminal-bench@2.0 regex-log" if ok else f"unexpected: {out.strip()[-300:]}")
