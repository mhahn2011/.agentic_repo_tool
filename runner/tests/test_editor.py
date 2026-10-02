"""E-009 real editor: prompt content and reply parsing, with an injected runner (no live call)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import skill_loop  # noqa: E402

TRIALS = [{"passed": True, "turns": 4, "tps": 10, "feedback": {k: k + "!" for k in skill_loop.KEYS}}] * 3
REPLY = "## CHANGELOG\nacted on: 1,2\nrejected: 3\npredict: fewer turns\nagreed: 2\nchanged: yes\n## SKILL\nnew text"


class EditorTests(unittest.TestCase):
    def test_changed(self):
        seen = {}
        ed = skill_loop.make_editor(run=lambda cmd, p: seen.update(cmd=cmd, p=p) or REPLY)
        r = ed("old", TRIALS)
        self.assertEqual((r["skill"], r["changed"], r["agreed"]), ("new text", True, 2))
        self.assertIn("old", seen["p"])
        self.assertIn("helped!", seen["p"])
        self.assertIn("--tools", seen["cmd"])

    def test_no_change_keeps_skill(self):
        r = skill_loop.make_editor(run=lambda c, p: REPLY.replace("yes", "no"))("old", TRIALS)
        self.assertEqual((r["skill"], r["changed"]), ("old", False))

    def test_garbage_is_no_change(self):
        r = skill_loop.make_editor(run=lambda c, p: "???")("old", TRIALS)
        self.assertEqual((r["skill"], r["changed"]), ("old", False))


if __name__ == "__main__":
    unittest.main()
