"""C1.11 Run record complete, using the FAKE claude (no real session)."""
import json
import tempfile
from pathlib import Path

from common import PY, ROOT, finish, sh

fake = ROOT / "runner" / "tests" / "fake_claude.py"
out_dir = Path(tempfile.mkdtemp())
rc, out = sh([PY, str(ROOT / "runner" / "run_trial.py"), "mm-arrow/01-version-relocate", "L0", "haiku", "1",
              "--claude-bin", str(fake), "--out-dir", str(out_dir), "--timeout", "120"], timeout=600)
recs = list(out_dir.rglob("record.json"))
if not recs:
    finish(False, f"runner rc={rc}, no record.json: {out[-400:]}")
r = json.loads(recs[0].read_text(encoding="utf-8"))


def dig(d, path):
    for k in path.split("."):
        if not isinstance(d, dict) or d.get(k) is None:
            return None
        d = d[k]
    return d


need = ["model_resolved", "claude_code_version", "tokens.input", "tokens.output", "turns", "wall_s",
        "exit_status", "grader.deterministic.pass", "rate_limit", "total_cost_usd"]
missing = [k for k in need if dig(r, k) is None]
finish(not missing, f"missing/null: {missing}" if missing else f"complete record at {recs[0]}")
