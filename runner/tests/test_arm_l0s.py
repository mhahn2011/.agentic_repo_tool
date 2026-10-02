"""K4: arm L0S differs from L0 only by prompt_prefix (and name/description/status text)."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "runner"))

import run_trial  # noqa: E402

IDENTITY_ONLY = {"name", "description", "isolation_status", "prompt_prefix"}


class ArmL0S(unittest.TestCase):
    def setUp(self):
        self.l0 = run_trial.load_arm("L0")
        self.l0s = run_trial.load_arm("L0S")

    def test_resolved_flag_lists_identical(self):
        claude = ["claude"]
        self.assertEqual(run_trial.build_cmd(claude, self.l0, "haiku"),
                         run_trial.build_cmd(claude, self.l0s, "haiku"))

    def test_only_identity_and_prefix_keys_differ(self):
        keys = set(self.l0) | set(self.l0s)
        differing = {k for k in keys if self.l0.get(k) != self.l0s.get(k)}
        self.assertLessEqual(differing, IDENTITY_ONLY)
        self.assertIn("prompt_prefix", differing)

    def test_prefix_carries_skill_placeholder(self):
        self.assertIn("{SKILL}", self.l0s["prompt_prefix"])
        self.assertEqual(self.l0s["level"], "L0")


if __name__ == "__main__":
    unittest.main()
