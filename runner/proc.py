"""Run the agent process and stop at its `result` event (E-008, TCD-020_01).

Seen live 2026-10-01 (trial mm-arrow/05 L0, claude 2.1.284 in docker): the session emitted `result` success at 139 s
but the process never exited, so subprocess.run waited for the 900 s timeout and the trial was misfiled as `timeout`.
Here stdout is read line by line; once a `result` line arrives the process gets `grace` seconds to exit, then it is
killed and the trial is marked hung_after_result (graded normally, the hang stays countable).
"""
import json
import subprocess
import threading
import time


def _is_result(line: str) -> bool:
    line = line.strip()
    if not line.startswith("{"):
        return False
    try:
        obj = json.loads(line)
    except ValueError:
        return False
    return isinstance(obj, dict) and obj.get("type") == "result"


def run_until_result(argv, prompt, timeout, grace=30, cwd=None, env=None):
    """Returns dict: exit_code, stdout, stderr, timed_out, hung_after_result. Raises OSError if argv cannot launch."""
    p = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                         encoding="utf-8", errors="replace", cwd=cwd, env=env)
    out, err, got_result = [], [], threading.Event()

    def read_out():
        for line in p.stdout:
            out.append(line)
            if _is_result(line):
                got_result.set()

    def read_err():
        err.append(p.stderr.read())

    readers = [threading.Thread(target=read_out, daemon=True), threading.Thread(target=read_err, daemon=True)]
    for t in readers:
        t.start()
    try:
        p.stdin.write(prompt or "")
        p.stdin.close()
    except OSError:
        pass  # process already gone; its output says why

    deadline = time.time() + timeout
    timed_out = hung = False
    while p.poll() is None:
        if got_result.is_set():
            try:
                p.wait(timeout=grace)
            except subprocess.TimeoutExpired:
                hung = True
            break
        if time.time() >= deadline:
            timed_out = True
            break
        got_result.wait(timeout=0.5)
    if p.poll() is None:
        p.kill()
        p.wait()
    for t in readers:
        t.join(timeout=10)
    for f in (p.stdout, p.stderr):
        try:
            f.close()
        except (OSError, ValueError):
            pass
    return {"exit_code": -1 if timed_out else p.returncode, "stdout": "".join(out), "stderr": "".join(err),
            "timed_out": timed_out, "hung_after_result": hung}
