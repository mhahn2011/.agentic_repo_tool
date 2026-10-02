"""Fill CLAUDE_CODE_OAUTH_TOKEN from the macOS login Keychain when it is not in the environment.

Claude Code strips its own auth token from the shells its Bash tool spawns, so a relay hop that runs the harness
sees no token even though the hop itself was authenticated. The harness therefore fetches the token itself, inside
this process only: it is never printed, logged or written to disk, and the agent never handles it.
"""
import os
import subprocess
import sys

TOKEN_VAR = "CLAUDE_CODE_OAUTH_TOKEN"
KEYCHAIN_SERVICE = "claude-code-oauth"


def ensure_token() -> bool:
    """Return True if the token is available in os.environ after the call."""
    if os.environ.get(TOKEN_VAR):
        return True
    if sys.platform != "darwin":
        return False
    try:
        p = subprocess.run(["security", "find-generic-password", "-s", KEYCHAIN_SERVICE, "-w"],
                           capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return False
    value = (p.stdout or "").strip()
    if p.returncode == 0 and value:
        os.environ[TOKEN_VAR] = value
        return True
    return False
