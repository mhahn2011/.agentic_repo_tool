"""Generate the mm-arrow task folders. Re-run after editing TASKS. Tasks listed in MANUAL get reference/apply.py
(hand-written via handref.py) instead of relying on map-and-move; see FINDINGS.md for why."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# id, difficulty tags, moves, one-line description of what makes it interesting
TASKS = [
    ("01-version-relocate", "single module, one relative importer (re-export from __init__)",
     [("arrow/_version.py", "arrow/meta/_version.py")]),
    ("02-constants-many-importers", "single module, many absolute importers (6 source files + tests)",
     [("arrow/constants.py", "arrow/core/constants.py")]),
    ("03-util-module-style", "module imported both as 'from arrow.util import x' and 'from arrow import util'",
     [("arrow/util.py", "arrow/helpers/util.py")]),
    ("04-locales-module-style", "module imported via 'from arrow import a, b, locales' groups in library and tests",
     [("arrow/locales.py", "arrow/i18n/locales.py")]),
    ("05-parser-reexport", "module whose name is re-exported from __init__ (ParserError) and imported by tests",
     [("arrow/parser.py", "arrow/parsing/parser.py")]),
    ("06-formatter-multiline-reexport", "module re-exported by a multi-line relative import in __init__",
     [("arrow/formatter.py", "arrow/formatting/formatter.py")]),
    ("07-api-reexport", "public API module re-exported by relative import in __init__",
     [("arrow/api.py", "arrow/public/api.py")]),
    ("08-factory-mixed-imports", "module with absolute, module-style and relative importers",
     [("arrow/factory.py", "arrow/build/factory.py")]),
    ("09-two-modules", "two related modules moved into one new package in a single plan",
     [("arrow/parser.py", "arrow/text/parser.py"), ("arrow/formatter.py", "arrow/text/formatter.py")]),
    ("10-core-arrow-name-collision", "core module whose name equals its package (arrow.arrow); imported everywhere",
     [("arrow/arrow.py", "arrow/core/arrow.py")]),
]

MANUAL = set(json.loads((HERE / "manual.json").read_text())) if (HERE / "manual.json").exists() else set()

PROMPT = """You are working in a checkout of the Python library `arrow` (package `arrow/`, tests in `tests/`).

Task: relocate these module files, and update the rest of the repository so everything still works.

{moves}

Requirements:
- Every import of a moved module anywhere in the repository (library code and tests) must keep working from its new location. Update imports; do not leave compatibility stubs at the old paths.
- Do not delete, rename or weaken any test. The full test suite must still pass with the same number of passing tests as before you started (run it with `python -m pytest -q -o addopts=`).
- New package directories need an `__init__.py`.
- Do not commit. Work only inside this directory.

When finished, reply with one line saying what you moved."""


def main():
    for tid, why, moves in TASKS:
        d = HERE / tid
        (d / "reference").mkdir(parents=True, exist_ok=True)
        plan = {"moves": [{"from": a, "to": b} for a, b in moves]}
        (d / "reference" / "plan.json").write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
        exp = {"fixture": "arrow", "difficulty": why, "moves": plan["moves"],
               "must_exist": [b for _, b in moves] + sorted({str(Path(b).parent).replace("\\", "/") + "/__init__.py"
                                                              for _, b in moves}),
               "must_not_exist": [a for a, _ in moves]}
        (d / "expected.json").write_text(json.dumps(exp, indent=2) + "\n", encoding="utf-8")
        text = PROMPT.format(moves="\n".join(f"- `{a}` -> `{b}`" for a, b in moves))
        (d / "task.md").write_text(text + "\n", encoding="utf-8")
        apply = d / "reference" / "apply.py"
        if tid in MANUAL:
            apply.write_text(
                "import json, sys\nfrom pathlib import Path\n"
                "sys.path.insert(0, str(Path(__file__).resolve().parents[2]))\nimport handref\n"
                "handref.apply(json.loads((Path(__file__).parent / 'plan.json').read_text())['moves'])\n",
                encoding="utf-8")
        elif apply.exists():
            apply.unlink()
    print(f"built {len(TASKS)} tasks; manual references: {sorted(MANUAL)}")


if __name__ == "__main__":
    sys.exit(main())
