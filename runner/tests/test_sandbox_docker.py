"""Docker sandbox tests (fake claude inside a derived test image; no real session, no network to any API).
Run: python -m unittest discover -s runner/tests -p "test_sandbox*.py" -v     (needs Docker and the trial image)
Build the trial image first: python docker/trial-arrow/build.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "runner"))
import run_trial  # noqa: E402
import sandbox_docker as sd  # noqa: E402

TASK = "mm-arrow/01-version-relocate"
TEST_IMAGE = "e008/trial-arrow-test:1"
SENTINEL = "sk-ant-oat01-SENTINELTOKEN-do-not-leak-0123456789"
BAKED_KEY = "baked-api-key-should-be-stripped"
REF_CMD = ("python /opt/tools/script_map_and_move/cli/refactor_tool.py --plan /opt/testref/plan.json "
           "--root . --yes --no-commit")
DOCKERFILE = f"""FROM {sd.DEFAULT_IMAGE}
USER root
COPY fake_claude.py /opt/fake_claude.py
COPY plan.json /opt/testref/plan.json
COPY claude-fake /usr/local/bin/claude-fake
RUN chmod +x /usr/local/bin/claude-fake
ENV ANTHROPIC_API_KEY={BAKED_KEY}
USER trial
"""


def docker(*args, timeout=300):
    p = subprocess.run([sd.docker_bin(), *args], capture_output=True, text=True, encoding="utf-8", errors="replace",
                       timeout=timeout)
    return p.returncode, p.stdout + p.stderr


def setUpModule():
    if sd.image_id(sd.DEFAULT_IMAGE) is None:
        raise unittest.SkipTest(f"image {sd.DEFAULT_IMAGE} not built")
    ctx = Path(tempfile.mkdtemp())
    shutil.copy(HERE / "fake_claude.py", ctx)
    shutil.copy(ROOT / "tasks" / TASK / "reference" / "plan.json", ctx)
    shim = "#!/bin/sh" + chr(10) + 'exec python /opt/fake_claude.py "$@"' + chr(10)
    (ctx / "claude-fake").write_bytes(shim.encode())
    (ctx / "Dockerfile").write_text(DOCKERFILE, encoding="utf-8")
    rc, out = docker("build", "-q", "-t", TEST_IMAGE, str(ctx))
    assert rc == 0, out


def scratch() -> Path:
    """Dir for the /out bind mount. Must sit under $HOME: Colima/Docker Desktop on macOS only share the home
    directory with the VM (the system temp dir /var/folders is not shared, so the mount would be empty)."""
    base = ROOT / "runs" / "tmp"
    base.mkdir(parents=True, exist_ok=True)
    return Path(tempfile.mkdtemp(dir=base))


def trial(edit=None, extra_args=(), env=None):
    out = scratch()
    argv = [TASK, "L0", "haiku", "1", "--sandbox", "docker", "--image", TEST_IMAGE, "--container-claude",
            "claude-fake", "--out-dir", str(out), "--timeout", "600",
            "--container-env", "FAKE_ENV_OUT=/out/env.json", "--container-env", "FAKE_ARGV_OUT=/out/argv.json"]
    if edit:
        argv += ["--container-env", f"FAKE_EDIT_CMD={edit}"]
    old = {k: os.environ.get(k) for k in (env or {})}
    os.environ.update(env or {})
    try:
        rc = run_trial.main(argv + list(extra_args))
    finally:
        for k, v in old.items():
            os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)
    cell = next(out.rglob("record.json")).parent
    return rc, json.loads((cell / "record.json").read_text(encoding="utf-8")), cell


class SandboxTests(unittest.TestCase):
    def test_reference_tree_passes_in_container(self):
        rc, rec, cell = trial(edit=REF_CMD)
        self.assertEqual(rec["failure_class"], "pass", rec["grader"])
        self.assertTrue(rec["grader"]["deterministic"]["pass"])
        self.assertEqual(rec["sandbox"], "docker")
        self.assertTrue(rec["container_image"].startswith("sha256:"))
        self.assertIn("arrow/meta/_version.py", (cell / "workspace.diff").read_text(encoding="utf-8"))

    def test_untouched_tree_fails_in_container(self):
        rc, rec, _ = trial()
        self.assertFalse(rec["grader"]["deterministic"]["pass"])
        self.assertEqual(rec["failure_class"], "fail")

    def test_container_removed_and_token_handling(self):
        env = {sd.TOKEN_VAR: SENTINEL}
        rc, rec, cell = trial(env=env, extra_args=["--keep"])
        seen = json.loads((cell / "env.json").read_text(encoding="utf-8"))
        self.assertEqual(seen[sd.TOKEN_VAR], SENTINEL)  # delivered at runtime
        self.assertIsNone(seen["ANTHROPIC_API_KEY"])  # baked into the image, stripped by env -u
        self.assertIn("--safe-mode", json.loads((cell / "argv.json").read_text(encoding="utf-8")))
        rc, names = docker("ps", "-aq", "--filter", "label=e008=trial")
        ids = names.split()
        self.assertEqual(len(ids), 1, "--keep must leave exactly this container")
        rc, cinspect = docker("inspect", ids[0])
        self.assertNotIn(SENTINEL, cinspect)
        docker("rm", "-f", ids[0])
        for target in (TEST_IMAGE, sd.DEFAULT_IMAGE):
            self.assertNotIn(SENTINEL, docker("inspect", target)[1])
            self.assertNotIn(SENTINEL, docker("history", "--no-trunc", target)[1])
        for f in cell.iterdir():
            if f.name in ("env.json", "argv.json"):
                continue  # written on purpose by the fake to prove what the agent process saw
            self.assertNotIn(SENTINEL, f.read_text(encoding="utf-8", errors="replace"), f.name)
        # and without --keep nothing is left behind
        trial()
        self.assertEqual(docker("ps", "-aq", "--filter", "label=e008=trial")[1].split(), [])

    def test_grader_files_not_in_image(self):
        rc, out = docker("run", "--rm", sd.DEFAULT_IMAGE, "sh", "-c", "ls /opt/grader /opt/testref 2>&1; id -u")
        self.assertIn("1000", out)  # non-root
        rc, out = docker("run", "--rm", sd.DEFAULT_IMAGE, "sh", "-c", "ls /opt/grader | wc -l")
        self.assertEqual(out.strip(), "0")

    def test_real_claude_needs_live_and_token(self):
        out = Path(tempfile.mkdtemp())
        old = os.environ.pop(sd.TOKEN_VAR, None)
        try:
            rc = run_trial.main([TASK, "L0", "haiku", "1", "--sandbox", "docker", "--out-dir", str(out)])
            rc2 = run_trial.main([TASK, "L0", "haiku", "1", "--sandbox", "docker", "--live", "--out-dir", str(out)])
        finally:
            if old:
                os.environ[sd.TOKEN_VAR] = old
        self.assertEqual((rc, rc2), (77, 77))
        self.assertEqual(list(out.rglob("record.json")), [])

    def test_in_container_baseline_and_cli(self):
        rc, out = docker("run", "--rm", sd.DEFAULT_IMAGE, "sh", "-c",
                         "claude --version; PYTHONPATH=. python -m pytest -q -p no:cacheprovider -o addopts= | tail -1")
        self.assertIn("1865 passed", out)  # Linux baseline; Windows host is 1862 passed / 1 skipped
        self.assertRegex(out, r"2\.1\.284")


if __name__ == "__main__":
    unittest.main()
