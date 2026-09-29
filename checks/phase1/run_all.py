"""Run every Phase 1 check; print a status table. Exit 0 only if nothing FAILED (BLOCKED is reported, not failed)."""
import subprocess
import sys
from pathlib import Path

here = Path(__file__).parent
rows, failed = [], False
for f in sorted(here.glob("c1_*.py")):
    p = subprocess.run([sys.executable, str(f)], capture_output=True, text=True, cwd=here, timeout=3600)
    status = {0: "PASS", 77: "BLOCKED"}.get(p.returncode, "FAIL")
    failed |= status == "FAIL"
    first = ((p.stdout or p.stderr).strip().splitlines() or [""])[0]
    rows.append((f.stem, status, first))
for name, status, first in rows:
    print(f"{name:24} {status:8} {first[:100]}")
sys.exit(1 if failed else 0)
