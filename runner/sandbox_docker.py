"""Docker sandbox for one trial (E-008, TCD-020_01 Phase 1b).

One fresh container per trial, created from an image that holds the pinned fixture with its .git, test deps, the
claude CLI and the map-and-move tool, but NOT the tasks, expected.json or reference solutions. Flow:
  create (only mount: an output dir at /out) -> start -> exec the agent (prompt on stdin) -> docker cp the grader
  in -> exec the grader on the resulting tree -> write the diff to /out -> remove the container.
The OAuth token is passed ONLY as `docker exec -e CLAUDE_CODE_OAUTH_TOKEN` (value inherited from this process's
environment, never on a command line), so it is in neither the image, the container config nor `docker history`.
ANTHROPIC_API_KEY / ANTHROPIC_AUTH_TOKEN are removed inside the container with `env -u`.
"""
import json
import os
import shutil
import subprocess
import uuid
from pathlib import Path

from proc import run_until_result
from keychain_token import ensure_token

DEFAULT_IMAGE = "e008/trial-arrow:1"
# not on PATH in some shells: Docker Desktop (Windows), Homebrew (Intel / Apple silicon macOS)
DOCKER_DIRS = (r"C:\Program Files\Docker\Docker\resources\bin", "/usr/local/bin", "/opt/homebrew/bin")
TOKEN_VAR = "CLAUDE_CODE_OAUTH_TOKEN"
ensure_token()  # macOS: fetch from the Keychain if Claude Code stripped it from this shell
STRIP_VARS = ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")
WORKDIR = "/work/arrow"


def docker_bin() -> str:
    found = shutil.which("docker")
    for d in DOCKER_DIRS:
        found = found or shutil.which("docker", path=d)
    if not found:
        raise RuntimeError("docker not found (not on PATH or in the usual Docker Desktop / Homebrew dirs)")
    return found


def _docker(args, timeout=120, input_text=None, env=None):
    p = subprocess.run([docker_bin()] + [str(x) for x in args], capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=timeout, input=input_text, env=env)
    return p.returncode, p.stdout, p.stderr


def image_id(image: str):
    rc, out, _ = _docker(["image", "inspect", "--format", "{{.Id}}", image], timeout=60)
    return out.strip() if rc == 0 else None


def agent_exec_args(name, cmd, extra_env):
    """Args for `docker exec` of the agent. Token is named without a value so docker reads it from our env."""
    args = ["exec", "-i"]
    if os.environ.get(TOKEN_VAR):
        args += ["-e", TOKEN_VAR]
    for k, v in sorted(extra_env.items()):
        args += ["-e", f"{k}={v}"]
    args += [name, "env"]
    for k in STRIP_VARS:
        args += ["-u", k]
    return args + list(cmd)


def run_in_container(image, cmd, prompt, extra_env, grader_root, task, out_dir, timeout, network=None, keep=False,
                     grace=30):
    """Returns dict: exit_code, stdout, stderr, timed_out, hung_after_result, launch_error, grade(dict|None), diff,
    image_id, name."""
    name = f"e008-trial-{uuid.uuid4().hex[:8]}"
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    res = {"exit_code": None, "stdout": "", "stderr": "", "timed_out": False, "hung_after_result": False, "launch_error": None, "grade": None,
           "diff": "", "image_id": image_id(image), "name": name}
    create = ["create", "--name", name, "--label", "e008=trial", "-v", f"{out_dir.resolve()}:/out"]
    if network:
        create += ["--network", network]
    try:
        rc, _, err = _docker(create + [image, "sleep", "infinity"])
        if rc:
            raise RuntimeError(f"docker create failed: {err.strip()[:300]}")
        rc, _, err = _docker(["start", name])
        if rc:
            raise RuntimeError(f"docker start failed: {err.strip()[:300]}")
        r = run_until_result([docker_bin()] + agent_exec_args(name, cmd, extra_env), prompt, timeout, grace)
        res.update(r)
        if r["timed_out"] or r["hung_after_result"]:
            # killing the docker CLI leaves the agent running in the container; stop it before grading
            _docker(["exec", name, "sh", "-c", "kill -9 -1"], timeout=30)
        res["grade"], res["diff"] = _grade_inside(name, grader_root, task, out_dir)
    except Exception as exc:  # noqa: BLE001 - recorded by the caller as harness_error
        res["launch_error"] = f"{type(exc).__name__}: {exc}"
    finally:
        if not keep:
            _docker(["rm", "-f", name], timeout=60)
    return res


def _grade_inside(name, grader_root, task, out_dir):
    """Copy grader + task + pins into the container (after the agent is done) and run it on /work/arrow."""
    g, root, tdir = "/opt/grader", Path(grader_root), Path(grader_root) / "tasks" / task
    _docker(["exec", name, "mkdir", "-p", f"{g}/runner", f"{g}/fixtures", f"{g}/tasks/{Path(task).parent}"])
    for src, dst in ((root / "runner" / "grade.py", f"{g}/runner/grade.py"),
                     (root / "fixtures" / "pins.json", f"{g}/fixtures/pins.json"),
                     (root / "fixtures" / "import_all.py", f"{g}/fixtures/import_all.py"),
                     (tdir, f"{g}/tasks/{task}")):
        rc, _, err = _docker(["cp", str(src), f"{name}:{dst}"])
        if rc:
            raise RuntimeError(f"docker cp {src.name} failed: {err.strip()[:200]}")
    rc, out, err = _docker(["exec", "-e", "E008_PYTHON=python", name, "python", f"{g}/runner/grade.py", task, WORKDIR],
                           timeout=900)
    try:
        grade = json.loads(out)
    except ValueError:
        grade = {"pass": False, "detail": {"grader_output": (out + err)[-400:]}}
    _docker(["exec", name, "sh", "-c", "git add --intent-to-add . && git diff HEAD > /out/workspace.diff"])
    df = out_dir / "workspace.diff"  # written by the container through the /out mount
    return grade, df.read_text(encoding="utf-8", errors="replace") if df.exists() else ""


def run_claude_once(image, cmd, prompt, setup=None, extra_env=None, timeout=300, network=None):
    """One throwaway container for the live checks: optional `setup` shell snippet (as the trial user), then the
    agent command with the prompt on stdin. No mounts. Returns {exit_code, stdout, stderr, env_seen} where
    env_seen lists the ANTHROPIC*/CLAUDE* variable NAMES visible to the agent process (never values)."""
    name = f"e008-once-{uuid.uuid4().hex[:8]}"
    res = {"exit_code": None, "stdout": "", "stderr": "", "env_seen": None}
    create = ["create", "--name", name, "--label", "e008=once"] + (["--network", network] if network else [])
    probe = "env | cut -d= -f1 | grep -E '^(ANTHROPIC|CLAUDE)'"
    try:
        rc, _, err = _docker(create + [image, "sleep", "infinity"])
        if rc:
            raise RuntimeError(f"docker create failed: {err.strip()[:300]}")
        _docker(["start", name])
        if setup:
            rc, _, err = _docker(["exec", name, "sh", "-c", setup])
            if rc:
                raise RuntimeError(f"setup failed: {err.strip()[:300]}")
        rc, out, _ = _docker(agent_exec_args(name, ["sh", "-c", probe], extra_env or {}))
        res["env_seen"] = sorted(out.split())
        p = subprocess.run([docker_bin()] + agent_exec_args(name, cmd, extra_env or {}), input=prompt,
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
        res.update(exit_code=p.returncode, stdout=p.stdout, stderr=p.stderr)
    finally:
        _docker(["rm", "-f", name], timeout=60)
    return res
