"""K1: skill-accretion loop driver tests (E-009). Fakes only: trial, editor and probe are injected.
Run: python3.12 -m unittest discover -s runner/tests -p 'test_skill_loop.py' -v"""
import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "runner"))

import skill_loop  # noqa: E402

TRAIN = ["03", "05", "07", "09", "10"]
HELD = ["01", "02", "04", "06", "08"]
GOOD_FB = "done\n## SKILL FEEDBACK\nhelped: a\nmissing: b\nwrong: c\nchange: d\n"


def trial_fn(passes=lambda task, version: True, feedback=GOOD_FB, log=None):
    def f(task, skill, version):
        if log is not None:
            log.append((task, version))
        return {"passed": passes(task, version), "tps": 100, "turns": 5, "final_text": feedback}
    return f


def editor(change=True, log=None):
    def f(skill, trials):
        if log is not None:
            log.append(len(trials))
        return {"skill": skill + "x" if change else skill, "changed": change, "agreed": 2, "changelog": "c"}
    return f


def make(tmp, **kw):
    args = dict(train=TRAIN, held=HELD, trial=trial_fn(), edit=editor(), probe=lambda: 0.1, ceiling=0.9,
                out_dir=Path(tmp), cap=12)
    args.update(kw)
    return skill_loop.Driver(**args)


class FeedbackTests(unittest.TestCase):
    def test_parse(self):
        fb = skill_loop.parse_feedback(GOOD_FB)
        self.assertEqual(fb, {"helped": "a", "missing": "b", "wrong": "c", "change": "d"})

    def test_missing_recorded_not_fatal(self):
        self.assertIsNone(skill_loop.parse_feedback("no section here"))


class LoopTests(unittest.TestCase):
    def test_no_edit_until_three_notes(self):
        with tempfile.TemporaryDirectory() as t:
            sizes = []
            d = make(t, edit=editor(log=sizes), cap=1)
            d.run()
            self.assertEqual(sizes, [3])

    def test_missing_feedback_does_not_count_toward_three(self):
        with tempfile.TemporaryDirectory() as t:
            calls = []
            seen = {"n": 0}

            def tr(task, skill, version):
                seen["n"] += 1
                bad = seen["n"] in (2, 5)  # trials 2 and 5 (sweep trials count too) lack feedback
                return {"passed": True, "tps": 1, "turns": 1, "final_text": "nope" if bad else GOOD_FB}
            d = make(t, trial=tr, edit=editor(log=calls), cap=1)
            d.run()
            self.assertTrue(all(n >= 3 for n in calls))

    def test_train_rotation(self):
        with tempfile.TemporaryDirectory() as t:
            log = []
            d = make(t, trial=trial_fn(log=log), cap=2)
            d.run()
            train_runs = [task for task, _v in log if task in TRAIN]
            cyc1, cyc2 = train_runs[5:8], train_runs[8:11]  # after the v0 sweep's 5 train trials
            self.assertEqual(len(set(cyc1)), 3)
            self.assertTrue(set(cyc1) != set(cyc2))

    def test_sweep_schedule(self):
        with tempfile.TemporaryDirectory() as t:
            d = make(t, cap=6)
            res = d.run()
            self.assertEqual(res["sweep_versions"], [0, 3, 6, res["final_version"]][: len(res["sweep_versions"])])
            self.assertEqual(res["sweep_versions"][:3], [0, 3, 6])

    def test_keep_best_revert(self):
        with tempfile.TemporaryDirectory() as t:
            # version 3 sweeps worse than version 0
            d = make(t, trial=trial_fn(passes=lambda task, v: not (v >= 3 and task in TRAIN)), cap=4)
            res = d.run()
            self.assertEqual(res["best_version"], 0)
            self.assertIn(3, res["reverted_from"])

    def test_stop_three_sweeps_without_new_best(self):
        with tempfile.TemporaryDirectory() as t:
            d = make(t, cap=12)  # constant results: v0 is best, nothing ever beats it
            res = d.run()
            self.assertEqual(res["stopped_by"], "no_new_best")

    def test_stop_two_no_change_cycles(self):
        with tempfile.TemporaryDirectory() as t:
            d = make(t, edit=editor(change=False), cap=12)
            self.assertEqual(d.run()["stopped_by"], "converged")

    def test_cap(self):
        with tempfile.TemporaryDirectory() as t:
            # always improving: pass count rises with version
            d = make(t, trial=trial_fn(passes=lambda task, v: TRAIN.index(task) < v if task in TRAIN else True), cap=2)
            self.assertEqual(d.run()["stopped_by"], "cap")

    def test_no_size_limits(self):
        with tempfile.TemporaryDirectory() as t:
            big = "line\n" * 5000
            d = make(t, edit=lambda s, tr: {"skill": big, "changed": True, "agreed": 3, "changelog": "c"}, cap=1)
            d.run()
            self.assertEqual((Path(t) / "skills" / "skill_g01.md").read_text(), big)

    def test_csv_rows(self):
        with tempfile.TemporaryDirectory() as t:
            make(t, cap=3).run()
            rows = list(csv.DictReader((Path(t) / "generations.csv").open()))
            kinds = [r["kind"] for r in rows]
            self.assertEqual(kinds.count("cycle"), 3)
            self.assertGreaterEqual(kinds.count("sweep"), 2)
            self.assertTrue({"version", "kind", "train_pass", "held_pass", "median_tps", "skill_lines"} <= set(rows[0]))


class QuotaTests(unittest.TestCase):  # K2
    def test_stops_before_launching_trial(self):
        with tempfile.TemporaryDirectory() as t:
            log = []
            d = make(t, probe=lambda: 0.895, trial=trial_fn(log=log))
            res = d.run()
            self.assertEqual(res["stopped_by"], "quota")
            self.assertEqual(log, [])


if __name__ == "__main__":
    unittest.main()
