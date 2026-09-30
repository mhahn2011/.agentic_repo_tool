"""C1.7 Subscription auth inside a container. Needs `--live` and CLAUDE_CODE_OAUTH_TOKEN, else exit 77.
Usage: python checks/phase1/c1_07_auth_container.py --live
Checks: claude -p "reply with the single word ok" (haiku) returns ok, is_error false; the agent process has no
ANTHROPIC_API_KEY; docker inspect/history of the image and `git grep` of the repo show no token string."""
import json
import os
import subprocess

from common import IMAGE, ROOT, TOKEN_VAR, finish, live_gate, sandbox

PROMPT_CMD = ["claude", "-p", "reply with the single word ok", "--output-format", "json", "--model", "haiku"]
live_gate("docker exec -e CLAUDE_CODE_OAUTH_TOKEN <fresh container> env -u ANTHROPIC_API_KEY " + " ".join(PROMPT_CMD))
sd = sandbox()
token = os.environ[TOKEN_VAR]
r = sd.run_claude_once(IMAGE, PROMPT_CMD, "", timeout=180)
problems = []
try:
    out = json.loads(r["stdout"])
    if out.get("is_error") or "ok" not in str(out.get("result", "")).lower():
        problems.append(f"bad result: is_error={out.get('is_error')} result={str(out.get('result'))[:80]!r}")
except ValueError:
    problems.append(f"no JSON (rc={r['exit_code']}): {r['stderr'][-200:]!r}")
if "ANTHROPIC_API_KEY" in (r["env_seen"] or []):
    problems.append("ANTHROPIC_API_KEY visible to the agent process")
if TOKEN_VAR not in (r["env_seen"] or []):
    problems.append("token not delivered to the agent process")
for args in (["image", "inspect", IMAGE], ["history", "--no-trunc", IMAGE]):
    p = subprocess.run([sd.docker_bin()] + args, capture_output=True, text=True, errors="replace")
    if token in p.stdout + p.stderr:
        problems.append(f"token found in docker {args[0]}")
g = subprocess.run(["git", "grep", "-F", "-e", token], cwd=ROOT, capture_output=True, text=True, errors="replace")
if g.returncode == 0:
    problems.append("token found in repo (git grep)")
finish(not problems, "; ".join(problems) or "auth ok in container, no API key, no token in image or repo")
