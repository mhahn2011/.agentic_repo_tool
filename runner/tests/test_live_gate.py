"""The live container checks must refuse (exit 77) unless BOTH --live and the token are present.
Never passes both: a test must not start a real session."""
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ["c1_06_auth_host.py", "c1_07_auth_container.py", "c1_09_l0_stripped.py", "c1_10_l0_canary.py", "smoke.py"]


def run(script, args, token):
    env = {k: v for k, v in os.environ.items() if k != "CLAUDE_CODE_OAUTH_TOKEN"}
    if token:
        env["CLAUDE_CODE_OAUTH_TOKEN"] = "dummy-not-a-real-token"
    return subprocess.run([sys.executable, str(ROOT / "checks" / "phase1" / script)] + args, capture_output=True,
                          text=True, env=env, timeout=60)


class LiveGate(unittest.TestCase):
    def test_blocked_without_flag_or_token(self):
        for s in SCRIPTS:
            for args, token in (([], False), (["--live"], False), ([], True)):
                p = run(s, args, token)
                self.assertEqual(p.returncode, 77, f"{s} {args} token={token}: {p.stdout[-200:]}{p.stderr[-200:]}")
                self.assertIn("BLOCKED", p.stdout)
                self.assertNotIn("dummy-not-a-real-token", p.stdout + p.stderr)


if __name__ == "__main__":
    unittest.main()
