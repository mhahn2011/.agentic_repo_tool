Task suites. `mm-arrow/` = map-and-move suite v0 on the pinned arrow fixture (H3 comparison). Each task folder:
`task.md` (agent prompt, arm-neutral), `expected.json` (moves + layout for the grader), `reference/` (`plan.json` for
map-and-move, or `apply.py` when map-and-move cannot do the move; see `mm-arrow/FINDINGS.md`).
Regenerate with `python tasks/mm-arrow/_build.py`. Validate graders with `python runner/validate_grader.py mm-arrow`.
