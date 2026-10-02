"""Shared helpers for Phase 1 checks (TCD-020_01). Each check exits 0 = pass, 1 = fail, 77 = BLOCKED."""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MISSIONHUB = Path(os.environ.get("E008_MISSIONHUB") or (Path.home() / "dev" / "MissionHub"))
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


# ---- live checks in a container (Phase 1b). Nothing below starts a session unless --live AND the token are present.
IMAGE = "e008/trial-arrow:1"
TOKEN_VAR = "CLAUDE_CODE_OAUTH_TOKEN"
sys.path.insert(0, str(ROOT / "runner"))
from keychain_token import ensure_token  # noqa: E402
ensure_token()  # macOS: fetch from the Keychain if Claude Code stripped it from this shell


def live_gate(would_run: str):
    """Exit 77 BLOCKED unless argv has --live and the OAuth token is in the environment (never printed)."""
    import os
    has_flag, has_tok = "--live" in sys.argv, bool(os.environ.get(TOKEN_VAR))
    if has_flag and has_tok:
        return
    missing = [m for m, ok in (("--live flag", has_flag), (TOKEN_VAR + " env var", has_tok)) if not ok]
    print("BLOCKED: awaiting approval for live trials (needs --live and a token)")
    print("missing:", ", ".join(missing))
    print("would run:", would_run)
    sys.exit(BLOCKED)


def sandbox():
    sys.path.insert(0, str(ROOT / "runner"))
    import sandbox_docker
    return sandbox_docker


def arm_cmd(arm_name: str, model: str = "haiku", claude: str = "claude"):
    sys.path.insert(0, str(ROOT / "runner"))
    import run_trial
    return run_trial.build_cmd([claude], run_trial.load_arm(arm_name), model)


def venv_py(name: str) -> Path:
    """Python of a fixture venv (Scripts/python.exe on Windows, bin/python elsewhere)."""
    sys.path.insert(0, str(ROOT / "runner"))
    import grade
    return Path(grade.venv_python(name, env={}))


def reset_cmd(name: str) -> list:
    """Command that restores a fixture to its pin (reset.ps1 on Windows, reset.sh elsewhere)."""
    if sys.platform == "win32":
        return ["powershell", "-NoProfile", "-File", str(ROOT / "fixtures" / "reset.ps1"), name]
    return ["sh", str(ROOT / "fixtures" / "reset.sh"), name]
