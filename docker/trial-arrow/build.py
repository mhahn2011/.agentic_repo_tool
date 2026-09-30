"""Build the trial image. Stages docker/trial-arrow/ctx (gitignored) from the pinned fixture and the tool.
Usage: python docker/trial-arrow/build.py [--tag e008/trial-arrow:1] [--cli-version 2.1.284]
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TOOL = ROOT / ".agentic_repo_tools/01_project_agnostic_system/01_composable_elements/01_tools/script_map_and_move"


def run(cmd, **kw):
    p = subprocess.run(cmd, **kw)
    if p.returncode:
        sys.exit(f"failed: {' '.join(map(str, cmd))}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="e008/trial-arrow:1")
    ap.add_argument("--cli-version", default="2.1.284")
    a = ap.parse_args()
    commit = json.loads((ROOT / "fixtures/pins.json").read_text(encoding="utf-8"))["arrow"]["commit"]
    ctx = HERE / "ctx"
    shutil.rmtree(ctx, ignore_errors=True)
    ctx.mkdir()
    run(["git", "clone", "--quiet", "--no-hardlinks", str(ROOT / "fixtures/arrow"), str(ctx / "arrow")])
    run(["git", "-C", str(ctx / "arrow"), "checkout", "--quiet", "--detach", commit])
    shutil.copytree(TOOL, ctx / "script_map_and_move", ignore=shutil.ignore_patterns("__pycache__", ".git", "*.pyc"))
    shutil.copy(HERE / "arrow-requirements.txt", ctx / "arrow-requirements.txt")
    run(["docker", "build", "-t", a.tag, "--build-arg", f"CLAUDE_CODE_VERSION={a.cli_version}",
         "-f", str(HERE / "Dockerfile"), str(ctx)])
    print("built", a.tag)


if __name__ == "__main__":
    main()
