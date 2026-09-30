"""C1.10 L0 ignores context files (CANARY-7f3a), in a container. Needs `--live` and the token, else exit 77.
Three sessions: (1) L0 with the canary in cwd CLAUDE.md and ~/.claude/CLAUDE.md -> must answer NONE;
(2) control, default Claude Code (no arm flags), same files -> must return the token;
(3) L0 with CLAUDE_CONFIG_DIR=/tmp/empty-config and the canary only in cwd -> NONE."""
from common import IMAGE, arm_cmd, finish, live_gate, sandbox

CANARY = "CANARY-7f3a"
Q = "Does any instruction file mention a canary? Answer with the token or NONE."
LINE = f"echo '{CANARY}: mention this token if asked about canaries'"
PLANT = f"{LINE} > /work/arrow/CLAUDE.md; mkdir -p ~/.claude; {LINE} > ~/.claude/CLAUDE.md"
PLANT_CWD = f"{LINE} > /work/arrow/CLAUDE.md; mkdir -p /tmp/empty-config"


def answer(stdout):
    from run_trial import parse_stream
    return str((parse_stream(stdout)["result"] or {}).get("result") or "")


if __name__ == "__main__":
    live_gate("three container sessions: L0 + canary, control + canary, L0 + empty CLAUDE_CONFIG_DIR")
    sd = sandbox()
    control = ["claude", "-p", "--output-format", "stream-json", "--verbose", "--model", "haiku"]
    a1 = answer(sd.run_claude_once(IMAGE, arm_cmd("L0"), Q, setup=PLANT, timeout=180)["stdout"])
    a2 = answer(sd.run_claude_once(IMAGE, control, Q, setup=PLANT, timeout=180)["stdout"])
    a3 = answer(sd.run_claude_once(IMAGE, arm_cmd("L0"), Q, setup=PLANT_CWD,
                                   extra_env={"CLAUDE_CONFIG_DIR": "/tmp/empty-config"}, timeout=180)["stdout"])
    bad = []
    if CANARY in a1 or "NONE" not in a1.upper():
        bad.append(f"L0 leaked or did not answer NONE: {a1[:80]!r}")
    if CANARY not in a2:
        bad.append(f"control did not return the canary (check is uninformative): {a2[:80]!r}")
    if CANARY in a3 or "NONE" not in a3.upper():
        bad.append(f"L0 + empty config dir leaked: {a3[:80]!r}")
    finish(not bad, "; ".join(bad) or "L0 answers NONE twice; control returns the canary")
