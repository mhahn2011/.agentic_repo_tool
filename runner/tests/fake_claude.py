"""Fake claude CLI for runner tests (pattern from MissionHub relay/tests/fake_claude.py). Never talks to any API.

Env controls:
  FAKE_MODE       ok (default) | sleep | rate | autherr | crash | hang (prints the result, then never exits)
  FAKE_EDIT_CMD   shell command run in cwd before answering (simulates the agent doing the work)
  FAKE_PROMPT_OUT file to write the stdin prompt to
  FAKE_ARGV_OUT   file to write argv (JSON) to
  FAKE_ENV_OUT    file to write selected env vars (JSON) to
"""
import json
import os
import subprocess
import sys
import time

prompt = sys.stdin.read()
mode = os.environ.get("FAKE_MODE", "ok")
if os.environ.get("FAKE_PROMPT_OUT"):
    open(os.environ["FAKE_PROMPT_OUT"], "w", encoding="utf-8").write(prompt)
if os.environ.get("FAKE_ARGV_OUT"):
    json.dump(sys.argv[1:], open(os.environ["FAKE_ARGV_OUT"], "w", encoding="utf-8"))
if os.environ.get("FAKE_ENV_OUT"):
    keys = ["ANTHROPIC_API_KEY", "CLAUDE_CODE_DISABLE_CLAUDE_MDS", "CLAUDE_CODE_OAUTH_TOKEN"]
    json.dump({k: os.environ.get(k) for k in keys} | {"cwd": os.getcwd()},
              open(os.environ["FAKE_ENV_OUT"], "w", encoding="utf-8"))

if mode == "sleep":
    time.sleep(60)
if mode == "crash":
    sys.stderr.write("boom\n")
    sys.exit(3)
if os.environ.get("FAKE_EDIT_CMD"):
    subprocess.run(os.environ["FAKE_EDIT_CMD"], shell=True, check=False, cwd=os.getcwd(),
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print(json.dumps({"type": "system", "subtype": "init", "session_id": "sess-fake", "model": "claude-fake-haiku-1",
                  "claude_code_version": "0.0.0-fake", "tools": ["Bash"], "mcp_servers": [], "plugins": [],
                  "slash_commands": []}))
now = int(time.time())
status = "rejected" if mode == "rate" else "allowed"
print(json.dumps({"type": "rate_limit_event", "rate_limit_info": {
    "status": status, "resetsAt": now + 600, "rateLimitType": "five_hour",
    "unifiedWindows": {"five_hour": {"utilization": 0.2, "resetsAt": now + 600},
                       "seven_day": {"utilization": 0.1, "resetsAt": now + 86400}}}}))
is_error = mode in ("rate", "autherr")
text = {"rate": "You've hit your usage limit", "autherr": "Invalid API key - please run /login"}.get(mode, "done")
print(json.dumps({"type": "result", "is_error": is_error, "result": text, "session_id": "sess-fake",
                  "num_turns": 4, "total_cost_usd": 0.0123, "duration_ms": 1500,
                  "usage": {"input_tokens": 100, "output_tokens": 50, "cache_creation_input_tokens": 10,
                            "cache_read_input_tokens": 200}}))
sys.stdout.flush()
if mode == "hang":  # seen live 2026-10-01: result emitted, process never exited
    time.sleep(60)
sys.exit(1 if is_error else 0)
