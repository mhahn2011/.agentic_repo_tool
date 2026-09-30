# map-and-move findings on arrow 1.4.0 (TCD-020_01, H3 input)

Tool: `.agentic_repo_tools/.../script_map_and_move/cli/refactor_tool.py`, run with `--yes --no-commit` on a fresh worktree.
Discovered with `python runner/validate_grader.py mm-arrow --map-and-move-only`. No tool code was changed (no fixes applied).

| Task | map-and-move result | Cause |
|---|---|---|
| 01 version-relocate | PASS | relative import in `__init__` handled |
| 02 constants-many-importers | PASS | `from arrow.constants import x` (absolute) handled, 6 importers + tests |
| 03 util, 04 locales, 05 parser, 06 formatter, 08 factory, 09 two-modules, 10 core-arrow | FAIL: import errors, 0 tests run | `from arrow import util, locales` (module imported through the package) is not recognised as an import of `arrow.util`; the statement is left pointing at the old location |
| 07 api-reexport | FAIL: 4 tests fail (1858 of 1862) | imports fixed, but `arrow.api` accessed as an attribute (`import arrow; arrow.api.get`) is not updated |

Bugs / limits recorded (all H3-relevant: the tool is a weaker helper than its README claims on real code):
1. **`from pkg import submodule` not rewritten.** The dominant import form in arrow. Not a small fix: `find_importers`
   matches `imp.module` only, and the per-line grouping in `rewrite_imports_for_move` replaces the whole statement
   with just the relevant names, which would drop the other names on the same line.
2. **False success.** The tool prints "Import verification complete" and "Refactoring complete" while the tree has broken imports.
3. **Attribute-style references and dotted strings** (`arrow.api.get`, `mocker.patch("arrow.parser.X")`) are not updated.
4. Creates a git checkpoint and a post-refactor commit by default (use `--no-commit`); prints "Moved" twice.
5. Name collision (`arrow.arrow`) breaks it as a special case of 1.

Consequence for the suite: references for tasks 03-10 are hand-written with `tasks/mm-arrow/handref.py` (ast-based, handles
1 and 3). H3 (map-and-move vs plain `git mv` + grep/sed) will be tested against a tool that solves only 2 of 10 tasks
unaided; L1 agents must be told (the prompt says so) to verify its output.
