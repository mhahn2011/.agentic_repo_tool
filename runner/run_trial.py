"""Run one trial: fresh git worktree of the pinned fixture, claude -p (prompt on stdin), grade, record, clean up.

Usage: python run_trial.py <task> <arm> <model> <trial#> [--claude-bin PATH] [--timeout S] [--out-dir DIR] [--keep]
  task  e.g. mm-arrow/02-constants-many-importers  (folder under tasks/)
  arm   L0 | L1  (arms/<arm>.json)

Phase 1a: only ever tested against runner/tests/fake_claude.py. Running it against the real claude.exe needs
Michael's sign-off (see TCD-020_01, "Blocked on approval: live trials").
RISK: this runs the agent on the HOST, not in a container. The deny list is a speed bump, not a sandbox.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import grade as grader  # noqa: E402

DEFAULT_CLAUDE = r"C:\Users\willi\.local\bin\claude.exe"
REJECT_RE = re.compile(r"rate.?limit|usage limit|limit (reached|exceeded)|hit your limit|too many requests|429", re.I)
AUTH_RE = re.compile(r"invalid api key|not logged in|please run /login|authentication|unauthorized|401|oauth token", re.I)


# ---------------------------------------------------------------- pure helpers (unit tested)

def load_arm(name: str) -> dict:
    return json.loads((ROOT / "arms" / f"{name}.json").read_text(encoding="utf-8"))


def resolve_claude(arg) -> list:
    cand = arg or os.environ.get("E008_CLAUDE_BIN") or DEFAULT_CLAUDE
    if cand.lower().endswith(".py"):  # a python script standing in for claude (tests)
        return [sys.executable, cand]
    return [cand]


def build_cmd(claude: list, arm: dict, model: str) -> list:
    cmd = list(claude) + ["-p", "--output-format", "stream-json", "--verbose", "--model", model] + list(arm["flags"])
    if arm.get("allowed_tools"):
        cmd += ["--allowedTools", ",".join(arm["allowed_tools"])]
    if arm.get("deny_tools"):
        cmd += ["--disallowedTools", ",".join(arm["deny_tools"])]
    return cmd


def parse_stream(stdout: str) -> dict:
    """Return {"init": dict|None, "result": dict|None, "rate_limit": dict|None} from stream-json output."""
    out = {"init": None, "result": None, "rate_limit": None}
    for line in (stdout or "").splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
        except ValueError:
            continue
        if not isinstance(obj, dict):
            continue
        t = obj.get("type")
        if t == "system" and obj.get("subtype") == "init":
            out["init"] = obj
        elif t == "result":
            out["result"] = obj
        elif t == "rate_limit_event" and isinstance(obj.get("rate_limit_info"), dict):
            out["rate_limit"] = obj["rate_limit_info"]
    return out


def classify(timed_out, exit_code, parsed, grade_pass, launch_error) -> str:
    """pass | fail | timeout | harness_error | rate_limited | auth_error"""
    if launch_error:
        return "harness_error"
    if timed_out:
        return "timeout"
    res, rate = parsed["result"], parsed["rate_limit"] or {}
    text = str((res or {}).get("result") or "")
    errored = bool(res and res.get("is_error")) or (exit_code not in (0, None) and res is None)
    if errored or exit_code not in (0, None):
        rate_bad = bool(rate.get("status")) and not str(rate["status"]).startswith("allowed")
        if rate_bad or REJECT_RE.search(text):
            return "rate_limited"
        if AUTH_RE.search(text):
            return "auth_error"
        return "harness_error"
    if res is None:
        return "harness_error"
    return "pass" if grade_pass else "fail"


# ---------------------------------------------------------------- git worktree

def git(args, cwd=None, timeout=120):
    p = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                       timeout=timeout)
    return p.returncode, p.stdout + p.stderr


def make_worktree(fixture: str, commit: str) -> Path:
    src = ROOT / "fixtures" / fixture
    wt = Path(tempfile.gettempdir()) / f"e008-{fixture}-{uuid.uuid4().hex[:8]}"
    rc, out = git(["worktree", "add", "--detach", str(wt), commit], cwd=src)
    if rc != 0:
        raise RuntimeError(f"worktree add failed: {out}")
    return wt


def remove_worktree(fixture: str, wt: Path):
    src = ROOT / "fixtures" / fixture
    git(["worktree", "remove", "--force", str(wt)], cwd=src)
    if wt.exists():
        shutil.rmtree(wt, ignore_errors=True)
    git(["worktree", "prune"], cwd=src)


# ---------------------------------------------------------------- one trial

def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("task")
    ap.add_argument("arm")
    ap.add_argument("model")
    ap.add_argument("trial", type=int)
    ap.add_argument("--claude-bin", default=None)
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--out-dir", default=str(ROOT / "runs" / "adhoc"))
    ap.add_argument("--keep", action="store_true", help="keep the worktree for inspection")
    a = ap.parse_args(argv)

    task_dir = ROOT / "tasks" / a.task
    exp = json.loads((task_dir / "expected.json").read_text(encoding="utf-8"))
    arm = load_arm(a.arm)
    pin = grader.load_pins()[exp["fixture"]]

    prompt = arm.get("prompt_prefix", "")
    if arm.get("tool_path"):
        prompt = prompt.replace("{TOOL}", str(ROOT / arm["tool_path"]))
    prompt += (task_dir / "task.md").read_text(encoding="utf-8")

    cmd = build_cmd(resolve_claude(a.claude_bin), arm, a.model)
    env = dict(os.environ)
    for k in arm.get("env_unset", []):
        env.pop(k, None)
    env.update(arm.get("env", {}))

    rec = {"task_id": a.task, "suite": a.task.split("/")[0], "cell_id": f"{a.arm}-{a.model}-{a.task}",
           "trial": a.trial, "model_alias": a.model, "level": arm["level"], "tool_treatment": arm.get("tool_treatment"),
           "arm_config_hash": hashlib.sha256(json.dumps(arm, sort_keys=True).encode()).hexdigest()[:16],
           "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest()[:16],
           "host": platform.node(), "container_image": None,
           "started_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
    t0 = time.time()
    wt, launch_error, timed_out, exit_code, stdout, stderr = None, None, False, None, "", ""
    try:
        wt = make_worktree(exp["fixture"], pin["commit"])
        try:
            p = subprocess.run(cmd, input=prompt, capture_output=True, text=True, encoding="utf-8", errors="replace",
                               cwd=str(wt), timeout=a.timeout, env=env)
            exit_code, stdout, stderr = p.returncode, p.stdout, p.stderr
        except subprocess.TimeoutExpired as exc:
            timed_out, exit_code = True, -1
            stdout = exc.stdout.decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        except OSError as exc:
            launch_error = f"could not launch claude: {exc}"
        agent_s = time.time() - t0
        parsed = parse_stream(stdout)
        g = grader.grade(wt, task_dir)
        git(["add", "--intent-to-add", "."], cwd=wt)
        _, diff = git(["diff", "HEAD"], cwd=wt)
    except Exception as exc:  # noqa: BLE001 - any harness failure is recorded, never raised
        launch_error = launch_error or f"{type(exc).__name__}: {exc}"
        agent_s = time.time() - t0
        parsed = parse_stream(stdout)
        g, diff = {"pass": False, "detail": {"harness": str(exc)}}, ""

    res, init = parsed["result"] or {}, parsed["init"] or {}
    usage = res.get("usage") or {}
    resolved = init.get("model") or next(iter(res.get("modelUsage") or {}), None)
    rec.update(
        model_resolved=resolved or ("unknown" if launch_error else None),
        claude_code_version=init.get("claude_code_version") or ("unknown" if launch_error else None),
        ended_at=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        wall_s=round(time.time() - t0, 1), agent_s=round(agent_s, 1),
        turns=res.get("num_turns"),
        tokens={"input": usage.get("input_tokens"), "output": usage.get("output_tokens"),
                "cache_creation": usage.get("cache_creation_input_tokens"),
                "cache_read": usage.get("cache_read_input_tokens")},
        notional_cost_usd=res.get("total_cost_usd"), total_cost_usd=res.get("total_cost_usd"),
        rate_limit=parsed["rate_limit"] or {"status": None},
        exit_status=exit_code, harness_error=launch_error,
        failure_class=classify(timed_out, exit_code, parsed, g["pass"], launch_error),
        grader={"deterministic": {"pass": g["pass"], "detail": g["detail"]}},
    )
    if a.claude_bin and a.claude_bin.lower().endswith(".py") or launch_error:
        rec["note"] = "fake claude" if not launch_error else launch_error

    out = Path(a.out_dir) / a.task.replace("/", "__") / a.arm / a.model / str(a.trial)
    out.mkdir(parents=True, exist_ok=True)
    (out / "record.json").write_text(json.dumps(rec, indent=2), encoding="utf-8")
    (out / "transcript.jsonl").write_text(stdout, encoding="utf-8")
    (out / "workspace.diff").write_text(diff, encoding="utf-8")
    (out / "grader.json").write_text(json.dumps(g, indent=2), encoding="utf-8")
    if stderr:
        (out / "stderr.txt").write_text(stderr, encoding="utf-8")

    if wt is not None and not a.keep:
        remove_worktree(exp["fixture"], wt)
    print(f"{rec['failure_class']}: {out / 'record.json'}")
    return 0 if rec["failure_class"] in ("pass", "fail") else 1


if __name__ == "__main__":
    sys.exit(main())
