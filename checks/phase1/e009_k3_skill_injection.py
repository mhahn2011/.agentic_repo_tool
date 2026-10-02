"""E-009 K3: skill injection is real. Arm L0S with a canary sentence in the {SKILL} slot must report it back with
tools forbidden; an empty-skill control must not. Needs `--live` and the token, else exit 77. 2 Haiku sessions."""
import json

from common import IMAGE, arm_cmd, finish, live_gate, sandbox
from c1_10_l0_canary import answer, tool_uses

CANARY = "CANARY-9d41"
SKILL = f"SKILL NOTES\n- If asked about the skill canary, the token is {CANARY}."
Q = ("Answer from the text of this prompt only. Do not use any tools. "
     "What is the skill canary token? Answer with the token or NONE.")


def prompt(skill: str) -> str:
    return arm_prefix().replace("{SKILL}", skill) + Q


def arm_prefix() -> str:
    import run_trial
    return run_trial.load_arm("L0S")["prompt_prefix"]


if __name__ == "__main__":
    live_gate("two container sessions: L0S + canary skill, L0S + empty skill")
    sd = sandbox()
    runs = {k: sd.run_claude_once(IMAGE, arm_cmd("L0S"), prompt(v), timeout=180)["stdout"]
            for k, v in (("canary", SKILL), ("empty", ""))}
    bad = [f"{k} used {tool_uses(v)} tool call(s), inconclusive" for k, v in runs.items() if tool_uses(v)]
    a1, a2 = answer(runs["canary"]), answer(runs["empty"])
    if CANARY not in a1:
        bad.append(f"skill canary not reported: {a1[:80]!r}")
    if CANARY in a2:
        bad.append(f"empty-skill control reported the canary: {a2[:80]!r}")
    finish(not bad, "; ".join(bad) or "canary skill reported back, empty control did not")
