"""C1.9 L0 is stripped: parse the system/init message of a real L0 run in a container.
Needs `--live` and CLAUDE_CODE_OAUTH_TOKEN, else exit 77. check_init() is unit-tested offline.
In the container ~/.claude is empty by construction, so this isolates the flags, not the host config."""
import sys

from common import IMAGE, arm_cmd, finish, live_gate, sandbox


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
    live_gate("L0 arm command in a fresh container, prompt 'hi'; check_init(system/init)")
    sd = sandbox()
    import run_trial
    r = sd.run_claude_once(IMAGE, arm_cmd("L0"), "hi", timeout=180)
    init = run_trial.parse_stream(r["stdout"])["init"]
    if not init:
        finish(False, f"no init message (rc={r['exit_code']}): {r['stderr'][-200:]!r}")
    print("init keys:", sorted(init), file=sys.stderr)  # turns the guessed field names into observed ones
    bad = check_init(init, "haiku")
    finish(not bad, "; ".join(bad) or "L0 init: tools==[Bash], no mcp/plugins/skills")
