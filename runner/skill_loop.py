"""E-009 skill-accretion loop driver. Pure orchestration: trial, edit and probe are injected callables.

trial(task, skill, version) -> {"passed": bool, "tps": number, "turns": int, "final_text": str}
edit(skill, trials)         -> {"skill": str, "changed": bool, "agreed": int, "changelog": str}
probe()                     -> seven_day utilization (0..1)

A cycle = trials on rotating train tasks until 3 feedback notes exist for the current version, then one edit.
A sweep = every train and held task, n=1. Sweeps run at v0, after every 3rd revision, and at the end.
"""
import csv
import re
import statistics
from pathlib import Path

KEYS = ("helped", "missing", "wrong", "change")
NOTES_NEEDED = 3
MAX_TRIALS_PER_CYCLE = 6
SWEEP_EVERY = 3
NO_NEW_BEST_LIMIT = 3
NO_CHANGE_LIMIT = 2
QUOTA_MARGIN = 0.01
TPS_MARGIN = 0.10
FIELDS = ["version", "kind", "train_pass", "held_pass", "median_tps", "skill_lines", "agreed", "changed"]


def parse_feedback(text):
    """Return {helped, missing, wrong, change} from the '## SKILL FEEDBACK' section, or None if absent/incomplete."""
    m = re.search(r"##\s*SKILL FEEDBACK\s*\n(.*)", text or "", re.S | re.I)
    if not m:
        return None
    body = m.group(1)
    hits = list(re.finditer(r"^\s*(helped|missing|wrong|change)\s*:\s*", body, re.I | re.M))
    out = {}
    for i, h in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(body)
        out.setdefault(h.group(1).lower(), body[h.end():end].strip())
    return out if all(out.get(k) for k in KEYS) else None


class _Quota(Exception):
    pass


class Driver:
    def __init__(self, train, held, trial, edit, probe, ceiling, out_dir, cap):
        self.train, self.held, self.trial, self.edit, self.probe = list(train), list(held), trial, edit, probe
        self.ceiling, self.out, self.cap = ceiling, Path(out_dir), cap
        self.skill, self.version = "", 0
        self.best_skill, self.best_version, self.best_score = "", None, None
        self.rows, self.sweep_versions, self.reverted_from = [], [], []
        self.rot = 0

    def _save_skill(self):
        d = self.out / "skills"
        d.mkdir(parents=True, exist_ok=True)
        (d / f"skill_g{self.version:02d}.md").write_text(self.skill)

    def _run_trial(self, task):
        if self.probe() >= self.ceiling - QUOTA_MARGIN:
            raise _Quota()
        r = dict(self.trial(task, self.skill, self.version))
        r["task"] = task
        r["feedback"] = parse_feedback(r.get("final_text", ""))
        return r

    def _row(self, kind, train=None, held=None, tps=None, agreed="", changed=""):
        self.rows.append({"version": self.version, "kind": kind, "train_pass": "" if train is None else train,
                          "held_pass": "" if held is None else held,
                          "median_tps": "" if not tps else statistics.median(tps),
                          "skill_lines": len(self.skill.splitlines()), "agreed": agreed, "changed": changed})
        with (self.out / "generations.csv").open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()
            w.writerows(self.rows)

    def _better(self, a, b):
        """a=(train_pass, median_tps) strictly better than b (None = nothing yet)."""
        if b is None or a[0] > b[0]:
            return True
        return a[0] == b[0] and a[1] is not None and b[1] and a[1] <= b[1] * (1 - TPS_MARGIN)

    def _worse(self, a, b):
        return a[0] < b[0] or (a[0] == b[0] and a[1] and b[1] and a[1] >= b[1] * (1 + TPS_MARGIN))

    def _sweep(self):
        tr = [self._run_trial(t) for t in self.train]
        he = [self._run_trial(t) for t in self.held]
        score = (sum(bool(r["passed"]) for r in tr), statistics.median([r["tps"] for r in tr]))
        self.sweep_versions.append(self.version)
        self._row("sweep", score[0], sum(bool(r["passed"]) for r in he), [r["tps"] for r in tr + he])
        new_best = self._better(score, self.best_score)
        if new_best:
            self.best_score, self.best_version, self.best_skill = score, self.version, self.skill
            self.no_new_best = 0
        else:
            self.no_new_best += 1
            if self._worse(score, self.best_score):
                self.reverted_from.append(self.version)
                self.skill = self.best_skill
        self.swept_current = True

    def _cycle(self):
        trials, notes = [], 0
        while notes < NOTES_NEEDED and len(trials) < MAX_TRIALS_PER_CYCLE:
            task = self.train[self.rot % len(self.train)]
            self.rot += 1
            r = self._run_trial(task)
            trials.append(r)
            notes += r["feedback"] is not None
        passes = sum(bool(r["passed"]) for r in trials)
        tps = [r["tps"] for r in trials]
        if notes < NOTES_NEEDED:
            self._row("cycle", passes, None, tps, 0, False)
            return False
        res = self.edit(self.skill, trials)
        changed = bool(res.get("changed")) and res["skill"] != self.skill
        if changed:
            self.skill, self.version = res["skill"], self.version + 1
            self._save_skill()
            self.swept_current = False
        with (self.out / "changelog.md").open("a") as f:
            f.write(f"## v{self.version} (agreed {res.get('agreed')}/3, changed={changed})\n{res.get('changelog', '')}\n\n")
        self._row("cycle", passes, None, tps, res.get("agreed"), changed)
        return changed

    def _result(self, stopped_by):
        return {"stopped_by": stopped_by, "best_version": self.best_version, "final_version": self.version,
                "sweep_versions": self.sweep_versions, "reverted_from": self.reverted_from}

    def run(self):
        self.out.mkdir(parents=True, exist_ok=True)
        self.no_new_best, self.swept_current, no_change, cycles = 0, False, 0, 0
        try:
            self._save_skill()
            self._sweep()
            while True:
                if self.no_new_best >= NO_NEW_BEST_LIMIT:
                    return self._result("no_new_best")
                if no_change >= NO_CHANGE_LIMIT:
                    stop = "converged"
                    break
                if cycles >= self.cap:
                    stop = "cap"
                    break
                changed = self._cycle()
                cycles += 1
                no_change = 0 if changed else no_change + 1
                if changed and self.version % SWEEP_EVERY == 0:
                    self._sweep()
            if not self.swept_current:
                self._sweep()
            return self._result(stop)
        except _Quota:
            return self._result("quota")


def make_trial(runs_dir, arm="L0S", model="haiku", extra_args=()):
    """Real trial callable: one run_trial.py trial with the skill injected and the feedback request appended.
    Default is a live Docker trial (needs the token env var); tests pass extra_args for the fake claude.
    tps = input + output + cache_creation tokens (uncached cost; the skill's own tokens are inside it)."""
    import json
    import tempfile

    import run_trial
    live = ["--sandbox", "docker", "--live"] if "--claude-bin" not in extra_args else []
    counter = [0]

    def trial(task, skill, version):
        counter[0] += 1
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write(skill)
        try:
            run_trial.main([task, arm, model, str(counter[0]), "--out-dir", str(Path(runs_dir) / version),
                            "--skill-file", f.name, "--feedback-request", *live, *extra_args])
        finally:
            Path(f.name).unlink()
        d = Path(runs_dir) / version / task.replace("/", "__") / arm / model / str(counter[0])
        rec = json.loads((d / "record.json").read_text(encoding="utf-8"))
        tok = rec.get("tokens") or {}
        final = ""
        for line in (d / "transcript.jsonl").read_text(encoding="utf-8").splitlines():
            try:
                m = json.loads(line)
            except ValueError:
                continue
            if m.get("type") == "result":
                final = str(m.get("result") or "")
        return {"passed": bool(rec["grader"]["deterministic"]["pass"]),
                "tps": sum(tok.get(k) or 0 for k in ("input", "output", "cache_creation")),
                "turns": rec.get("turns"), "final_text": final}
    return trial


EDITOR_PROMPT = """You maintain a skill file (guidance text prepended to a weaker coding agent's prompt) for refactoring \
tasks on a Python codebase. Below are the current skill, then {n} solver trials: each has its outcome and the \
agent's own feedback on the skill. Decide what, if anything, to change. Write general guidance, never task answers \
or file names of specific tasks. You may restructure, shorten or lengthen freely.

Reply in exactly this form:
## CHANGELOG
acted on: <which notes you acted on>
rejected: <which notes you rejected and why>
predict: <what you expect to change>
agreed: <0-{n}, how many notes support the change you made>
changed: <yes|no>
## SKILL
<the full new skill text, or the unchanged skill>

CURRENT SKILL:
<<<
{skill}
>>>

TRIALS:
{trials}
"""


def _format_trials(trials):
    out = []
    for i, t in enumerate(trials, 1):
        fb = t.get("feedback") or {}
        out.append(f"[{i}] passed={t.get('passed')} turns={t.get('turns')} tokens={t.get('tps')}\n"
                   + "\n".join(f"  {k}: {fb.get(k, '(no note)')}" for k in KEYS))
    return "\n".join(out)


def parse_edit(reply, skill):
    """Parse the editor reply into the edit() result dict. An unparseable reply is no change."""
    m = re.search(r"##\s*CHANGELOG\s*\n(.*?)\n##\s*SKILL\s*\n(.*)", reply or "", re.S | re.I)
    if not m:
        return {"skill": skill, "changed": False, "agreed": 0, "changelog": "editor reply unparseable"}
    log, new = m.group(1).strip(), m.group(2).strip()
    new = re.sub(r"^```\w*\n|\n```$", "", new)
    agreed = re.search(r"agreed:\s*(\d)", log, re.I)
    yes = re.search(r"changed:\s*yes", log, re.I)
    return {"skill": new if yes else skill, "changed": bool(yes) and new != skill.strip(),
            "agreed": int(agreed.group(1)) if agreed else 0, "changelog": log}


def make_editor(model="sonnet", claude_bin="claude", run=None):
    """Real editor: one headless claude call, no tools, prompt on stdin. `run(cmd, prompt)` -> stdout is injectable."""
    import subprocess

    def default_run(cmd, prompt):
        return subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=600).stdout

    run = run or default_run

    def edit(skill, trials):
        prompt = EDITOR_PROMPT.format(n=len(trials), skill=skill or "(empty)", trials=_format_trials(trials))
        cmd = [claude_bin, "-p", "--model", model, "--tools", ""]
        return parse_edit(run(cmd, prompt), skill)
    return edit


def main(argv=None):
    import argparse
    import json
    import subprocess
    import sys

    ap = argparse.ArgumentParser(description="E-009 skill-accretion loop")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--ceiling", type=float, required=True, help="weekly seven_day ceiling from relay/pace.py")
    ap.add_argument("--cap", type=int, default=12)
    ap.add_argument("--probe", default=str(Path.home() / "dev/MissionHub/system/execution-context/relay/usage_probe.py"))
    a = ap.parse_args(argv)
    names = sorted(p.name for p in (Path(__file__).resolve().parents[1] / "tasks/mm-arrow").iterdir()
                   if p.is_dir() and p.name[:2].isdigit())
    ids = ["mm-arrow/" + n for n in names]
    train = [t for t in ids if t.split("/")[1][:2] in ("03", "05", "07", "09", "10")]
    held = [t for t in ids if t not in train]

    def probe():
        out = subprocess.run([sys.executable, a.probe], capture_output=True, text=True).stdout
        return float(json.loads(out)["seven_day"]["utilization"])

    out = Path(a.out_dir)
    drv = Driver(train, held, make_trial(out / "runs"), make_editor(), probe, a.ceiling, out, a.cap)
    res = drv.run()
    (out / "result.json").write_text(json.dumps(res, indent=2))
    print(json.dumps(res))


if __name__ == "__main__":
    main()
