"""Platform-neutrality tests (Phase 1c, Mac port): venv layout, default claude path, docker lookup, POSIX scripts."""
import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "runner"))

import grade  # noqa: E402
import run_trial  # noqa: E402
import sandbox_docker  # noqa: E402


class VenvLayout(unittest.TestCase):
    def test_windows_layout(self):
        p = grade.venv_python("arrow", platform="win32", env={})
        self.assertTrue(p.replace("\\", "/").endswith("fixtures/.venvs/arrow/Scripts/python.exe"), p)

    def test_posix_layout(self):
        for plat in ("darwin", "linux"):
            p = grade.venv_python("rich", platform=plat, env={})
            self.assertTrue(p.replace("\\", "/").endswith("fixtures/.venvs/rich/bin/python"), p)

    def test_env_override_wins(self):
        self.assertEqual(grade.venv_python("arrow", platform="darwin", env={"E008_PYTHON": "python"}), "python")

    def test_default_follows_running_platform(self):
        p = grade.venv_python("arrow", env={}).replace("\\", "/")
        self.assertIn("/Scripts/python.exe" if sys.platform == "win32" else "/bin/python", p)


class BaselineKey(unittest.TestCase):
    PIN = {"baseline_tests": {"passed": 1862}, "baseline_tests_linux": {"passed": 1865},
           "baseline_tests_darwin": {"passed": 1863}}

    def test_per_platform(self):
        self.assertEqual(grade.baseline_for(self.PIN, "win32")["passed"], 1862)
        self.assertEqual(grade.baseline_for(self.PIN, "linux")["passed"], 1865)
        self.assertEqual(grade.baseline_for(self.PIN, "darwin")["passed"], 1863)

    def test_falls_back_to_default(self):
        pin = {"baseline_tests": {"passed": 980}}
        for plat in ("win32", "linux", "darwin"):
            self.assertEqual(grade.baseline_for(pin, plat)["passed"], 980)


class DefaultClaude(unittest.TestCase):
    def test_windows_default(self):
        self.assertTrue(run_trial.default_claude("win32", home="C:/h").endswith("claude.exe"))

    def test_posix_default_under_home(self):
        p = run_trial.default_claude("darwin", home="/Users/x")
        self.assertEqual(p.replace("\\", "/"), "/Users/x/.local/bin/claude")

    def test_resolve_uses_env_then_default(self):
        with mock.patch.dict(os.environ, {"E008_CLAUDE_BIN": "/opt/c"}):
            self.assertEqual(run_trial.resolve_claude(None), ["/opt/c"])


class DockerLookup(unittest.TestCase):
    def test_falls_back_to_homebrew_dir_on_posix(self):
        calls = []

        def fake_which(cmd, path=None):
            calls.append(path)
            return "/usr/local/bin/docker" if path == "/usr/local/bin" else None
        with mock.patch.object(sandbox_docker.shutil, "which", fake_which):
            self.assertEqual(sandbox_docker.docker_bin(), "/usr/local/bin/docker")

    def test_missing_raises(self):
        with mock.patch.object(sandbox_docker.shutil, "which", lambda *a, **k: None):
            with self.assertRaises(RuntimeError):
                sandbox_docker.docker_bin()


@unittest.skipIf(sys.platform == "win32", "POSIX scripts")
class PosixScripts(unittest.TestCase):
    def test_scripts_exist_and_executable(self):
        for n in ("setup.sh", "reset.sh"):
            self.assertTrue(os.access(ROOT / "fixtures" / n, os.X_OK), n)

    def test_reset_unknown_fixture_exits_2(self):
        r = subprocess.run(["sh", str(ROOT / "fixtures" / "reset.sh"), "nonesuch"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2, r.stderr)


if __name__ == "__main__":
    unittest.main()
