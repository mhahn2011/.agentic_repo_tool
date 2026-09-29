"""Shared helpers for Phase 1 checks (TCD-020_01). Each check exits 0 = pass, 1 = fail, 77 = BLOCKED."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MISSIONHUB = Path(r"C:\Users\willi\dev\MissionHub")
BLOCKED = 77
PY = sys.executable


def decode(b: bytes) -> str:
    if b"\x00" in b:  # wsl.exe prints UTF-16LE
        return b.decode("utf-16-le", "replace")
    return b.decode("utf-8", "replace")


def sh(cmd, cwd=None, timeout=300, env=None):
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, timeout=timeout, env=env)
    except (OSError, subprocess.SubprocessError) as exc:
        return 127, f"{type(exc).__name__}: {exc}"
    return p.returncode, decode(p.stdout) + decode(p.stderr)


def finish(ok: bool, msg: str):
    print(("PASS: " if ok else "FAIL: ") + msg)
    sys.exit(0 if ok else 1)


def blocked(why: str, command: str):
    print("BLOCKED: awaiting approval for live trials")
    print("reason:", why)
    print("would run:", command)
    sys.exit(BLOCKED)


def pins():
    return json.loads((ROOT / "fixtures" / "pins.json").read_text(encoding="utf-8"))
