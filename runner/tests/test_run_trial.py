"""Runner tests (fake claude only; no real session). Run: python -m unittest discover -s runner/tests -v"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "runner"))
sys.path.insert(0, str(ROOT / "checks" / "phase1"))

import run_trial  # noqa: E402

FAKE = str(HERE / "fake_claude.py")
TASK = "mm-arrow/02-constants-many-importers"
TOOL = (ROOT / ".agentic_repo_tools/01_project_agnostic_system/01_composable_elements/01_tools/"
        "script_map_and_move/cli/refactor_tool.py")


def run(mode="ok", edit=None, task=TASK, arm="L0", timeout=300, extra_env=None, extra_args=()):
    out = Path(tempfile.mkdtemp())
    env = {"FAKE_MODE": mode, "FAKE_PROMPT_OUT": str(out / "prompt.txt"), "FAKE_ARGV_OUT": str(out / "argv.json"),
           "FAKE_ENV_OUT": str(out / "env.json")}
    if edit:
        env["FAKE_EDIT_CMD"] = edit
    env.update(extra_env or {})
    old = {k: os.environ.get(k) for k in env}
    os.environ.update(env)
    os.environ["ANTHROPIC_API_KEY"] = "sk-test-should-be-stripped"
    try:
        rc = run_trial.main([task, arm, "haiku", "1", "--claude-bin", FAKE, "--out-dir", str(out / "runs"),
                             "--timeout", str(timeout), *extra_args])
    finally:
        for k, v in old.items():
            os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)
        os.environ.pop("ANTHROPIC_API_KEY", None)
    rec = json.loads(next((out / "runs").rglob("record.json")).read_text(encoding="utf-8"))
    return rc, rec, out


class ParseTests(unittest.TestCase):
    def test_parse_stream(self):
        stream = "\n".join([
            json.dumps({"type": "system", "subtype": "init", "model": "m1", "claude_code_version": "9.9", "tools": ["Bash"]}),
            "not json",
            json.dumps({"type": "rate_limit_event", "rate_limit_info": {"status": "allowed", "rateLimitType": "five_hour"}}),
            json.dumps({"type": "result", "is_error": False, "num_turns": 2, "total_cost_usd": 0.5,
                        "usage": {"input_tokens": 1, "output_tokens": 2, "cache_creation_input_tokens": 3,
                                  "cache_read_input_tokens": 4}}),
        ])
        p = run_trial.parse_stream(stream)
        self.assertEqual(p["init"]["model"], "m1")
        self.assertEqual(p["result"]["num_turns"], 2)
        self.assertEqual(p["rate_limit"]["status"], "allowed")

    def test_empty_stream(self):
        p = run_trial.parse_stream("")
        self.assertIsNone(p["result"])


class CmdTests(unittest.TestCase):
    def test_l0_cmd_flags(self):
        arm = run_trial.load_arm("L0")
        cmd = run_trial.build_cmd(["claude"], arm, "haiku")
        self.assertIn("--output-format", cmd)
        self.assertEqual(cmd[cmd.index("--output-format") + 1], "stream-json")
        self.assertIn("--verbose", cmd)
        self.assertNotIn("--bare", cmd)
        self.assertEqual(cmd[cmd.index("--tools") + 1], "Bash")
        self.assertIn("--strict-mcp-config", cmd)
        self.assertIn("--disable-slash-commands", cmd)
        deny = cmd[cmd.index("--disallowedTools") + 1]
        for pat in ("Bash(rm -rf*)", "Bash(git push*)", "Bash(curl*)", "Bash(wget*)"):
            self.assertIn(pat, deny)
        # prompt goes on stdin, never argv: last arg must be a flag value, not free text
        self.assertNotIn("Move", " ".join(cmd))

    def test_l1_prompt_mentions_tool(self):
        arm = run_trial.load_arm("L1")
        self.assertIn("{TOOL}", arm["prompt_prefix"])
        self.assertTrue(arm["tool_path"].endswith("refactor_tool.py"))
        self.assertEqual(arm["level"], "L1")


class EndToEnd(unittest.TestCase):
    def test_record_fields_and_env(self):
        rc, rec, out = run()
        self.assertEqual(rec["model_resolved"], "claude-fake-haiku-1")
        self.assertEqual(rec["claude_code_version"], "0.0.0-fake")
        self.assertEqual(rec["tokens"], {"input": 100, "output": 50, "cache_creation": 10, "cache_read": 200})
        self.assertEqual(rec["turns"], 4)
        self.assertEqual(rec["total_cost_usd"], 0.0123)
        self.assertEqual(rec["rate_limit"]["status"], "allowed")
        self.assertEqual(rec["exit_status"], 0)
        self.assertFalse(rec["grader"]["deterministic"]["pass"])  # fake did nothing
        self.assertEqual(rec["failure_class"], "fail")
        env = json.loads((out / "env.json").read_text())
        self.assertIsNone(env["ANTHROPIC_API_KEY"], "API key must be stripped (D1)")
        self.assertIn("e008-", Path(env["cwd"]).name)  # ran in the fresh worktree
        self.assertTrue((out / "prompt.txt").read_text().strip())  # prompt arrived on stdin
        self.assertFalse(Path(env["cwd"]).exists(), "worktree cleaned up")

    def test_pass_when_agent_does_the_work(self):
        edit = f'python "{TOOL}" --plan "{ROOT / "tasks" / TASK / "reference" / "plan.json"}" --root . --yes --no-commit'
        rc, rec, _ = run(edit=edit)
        self.assertTrue(rec["grader"]["deterministic"]["pass"], rec["grader"])
        self.assertEqual(rec["failure_class"], "pass")
        self.assertEqual(rc, 0)

    def test_timeout(self):
        rc, rec, _ = run(mode="sleep", timeout=3)
        self.assertEqual(rec["failure_class"], "timeout")

    def test_rate_limited(self):
        rc, rec, _ = run(mode="rate")
        self.assertEqual(rec["failure_class"], "rate_limited")

    def test_auth_error(self):
        rc, rec, _ = run(mode="autherr")
        self.assertEqual(rec["failure_class"], "auth_error")

    def test_crash_is_harness_error(self):
        rc, rec, _ = run(mode="crash")
        self.assertEqual(rec["failure_class"], "harness_error")
        self.assertEqual(rec["exit_status"], 3)


class InitCheck(unittest.TestCase):
    def test_check_init(self):
        import c1_09_l0_stripped as c9
        good = {"tools": ["Bash"], "mcp_servers": [], "plugins": [], "slash_commands": [], "model": "claude-haiku-x"}
        self.assertEqual(c9.check_init(good, "haiku"), [])
        bad = dict(good, tools=["Bash", "Read"], mcp_servers=[{"name": "x"}])
        self.assertEqual(len(c9.check_init(bad, "haiku")), 2)


if __name__ == "__main__":
    unittest.main()


class HangAfterResultTests(unittest.TestCase):
    def test_hang_after_result_ends_trial_and_is_graded(self):
        rc, rec, _ = run(mode="hang", timeout=300, extra_args=("--result-grace", "2"))
        self.assertTrue(rec["hung_after_result"])
        self.assertLess(rec["wall_s"], 45)
        self.assertEqual(rec["failure_class"], "fail")  # untouched tree: graded, not "timeout"
        self.assertEqual(rec["turns"], 4)

    def test_clean_exit_not_flagged(self):
        rc, rec, _ = run(mode="ok")
        self.assertFalse(rec["hung_after_result"])

    def test_classify_hung_uses_grade(self):
        parsed = {"result": {"is_error": False, "result": "done"}, "rate_limit": None, "init": None}
        self.assertEqual(run_trial.classify(False, -9, parsed, True, None, hung_after_result=True), "pass")
        self.assertEqual(run_trial.classify(False, -9, parsed, True, None), "harness_error")
