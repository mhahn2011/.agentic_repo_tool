"""C1.9 L0 is stripped: parse the system/init message of a real L0 run. BLOCKED until live trials approved.
check_init() is exercised offline by runner/tests against a synthetic init message."""
import os

from common import blocked, finish


def check_init(init: dict, model: str = "") -> list:
    """Return a list of violations (empty = L0 is stripped). Field names are unverified until a live run."""
    bad = []
    if init.get("tools") != ["Bash"]:
        bad.append(f"tools={init.get('tools')}")
    if init.get("mcp_servers"):
        bad.append(f"mcp_servers={init.get('mcp_servers')}")
    if init.get("plugins"):
        bad.append(f"plugins={init.get('plugins')}")
    if init.get("slash_commands") or init.get("skills"):
        bad.append("slash_commands/skills present (compare with built-ins on first live run)")
    if model and model not in str(init.get("model", "")):
        bad.append(f"model={init.get('model')}")
    return bad


if __name__ == "__main__":
    if os.environ.get("E008_LIVE_APPROVED") != "1":
        blocked("needs a real L0 session",
                "python runner/run_trial.py <canary-task> L0 haiku 1, then check_init(init message)")
    finish(False, "live path not implemented in Phase 1a")
