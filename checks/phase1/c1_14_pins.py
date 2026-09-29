"""C1.14 Fixtures pinned: pins.json has 40-hex commits; reset.ps1 restores HEAD; tree clean.
Set E008_FIXTURES=arrow (comma list) to limit which fixtures are checked (default: all three)."""
import os
import re

from common import ROOT, finish, pins, sh

try:
    p = pins()
except OSError as exc:
    finish(False, f"fixtures/pins.json missing: {exc}")
names = os.environ.get("E008_FIXTURES", "arrow,httpie,rich").split(",")
problems = []
for name in names:
    e = p.get(name)
    if not e or not re.fullmatch(r"[0-9a-f]{40}", e.get("commit", "")) or not e.get("repo"):
        problems.append(f"{name}: bad pin entry {e}")
        continue
    fx = ROOT / "fixtures" / name
    (fx / "E008_DIRTY.txt").write_text("x", encoding="utf-8")  # prove the reset does something
    rc, out = sh(["powershell", "-NoProfile", "-File", str(ROOT / "fixtures" / "reset.ps1"), name])
    if rc != 0:
        problems.append(f"{name}: reset.ps1 rc={rc}: {out.strip()[-300:]}")
        continue
    _, head = sh(["git", "-C", str(fx), "rev-parse", "HEAD"])
    _, st = sh(["git", "-C", str(fx), "status", "--porcelain"])
    if head.strip() != e["commit"]:
        problems.append(f"{name}: HEAD {head.strip()} != pin")
    if st.strip():
        problems.append(f"{name}: dirty after reset: {st.strip()[:200]}")
finish(not problems, "; ".join(problems) or f"{names} pinned and reset clean")
