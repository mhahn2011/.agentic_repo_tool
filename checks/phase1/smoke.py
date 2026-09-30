"""6-trial smoke plan in containers: tasks 01, 02, 05 x arms L0, L1 x Haiku, 1 trial each.
Needs `--live` and CLAUDE_CODE_OAUTH_TOKEN, else exit 77 (prints the six commands it would run).
Run C1.9 and C1.10 first; do not run this if either fails. Usage: python checks/phase1/smoke.py --live [--out-dir DIR]
Exit 0 if every trial produced a record with failure_class pass or fail (harness errors = 0); the model's pass
rate is reported, not judged."""
import json
import subprocess
import sys
from pathlib import Path

from common import ROOT, finish, live_gate

TASKS = ["mm-arrow/01-version-relocate", "mm-arrow/02-constants-many-importers", "mm-arrow/05-parser-reexport"]
ARMS = ["L0", "L1"]
out_dir = sys.argv[sys.argv.index("--out-dir") + 1] if "--out-dir" in sys.argv else str(ROOT / "runs" / "smoke")
cmds = [[sys.executable, str(ROOT / "runner" / "run_trial.py"), t, arm, "haiku", "1", "--sandbox", "docker",
         "--live", "--out-dir", out_dir] for arm in ARMS for t in TASKS]
live_gate("\n  " + "\n  ".join(" ".join(c[1:]) for c in cmds))
rows, harness_errors = [], 0
for c in cmds:
    subprocess.run(c, cwd=ROOT, timeout=1800)
    task, arm = c[2], c[3]
    rec_path = Path(out_dir) / task.replace("/", "__") / arm / "haiku" / "1" / "record.json"
    if not rec_path.exists():
        harness_errors += 1
        rows.append((task, arm, "NO RECORD", None, None))
        continue
    r = json.loads(rec_path.read_text(encoding="utf-8"))
    harness_errors += r["failure_class"] not in ("pass", "fail")
    rows.append((task, arm, r["failure_class"], r.get("wall_s"), r.get("tokens")))
for row in rows:
    print(*row, sep=" | ")
finish(harness_errors == 0, f"{len(rows)} trials, harness errors={harness_errors}")
