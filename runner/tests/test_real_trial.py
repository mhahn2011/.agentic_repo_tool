"""E-009 real trial callable (fake claude, no live session)."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "runner"))
sys.path.insert(0, str(HERE))

import skill_loop  # noqa: E402
from test_run_trial import FAKE, TASK  # noqa: E402


class RealTrial(unittest.TestCase):
    def test_trial_injects_skill_and_feedback_request(self):
        out = Path(tempfile.mkdtemp())
        env = {"FAKE_PROMPT_OUT": str(out / "prompt.txt")}
        os.environ.update(env)
        try:
            trial = skill_loop.make_trial(out / "runs", extra_args=["--claude-bin", FAKE])
            r = trial(TASK, "SKILL-TEXT-XYZ", "v0")
        finally:
            os.environ.pop("FAKE_PROMPT_OUT", None)
        prompt = (out / "prompt.txt").read_text()
        self.assertTrue(prompt.startswith("SKILL-TEXT-XYZ"))
        self.assertIn("## SKILL FEEDBACK", prompt)
        self.assertNotIn("{SKILL}", prompt)
        self.assertEqual(set(r), {"passed", "tps", "turns", "final_text"})
        self.assertIsInstance(r["passed"], bool)


if __name__ == "__main__":
    unittest.main()
