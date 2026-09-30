You are working in a checkout of the Python library `arrow` (package `arrow/`, tests in `tests/`).

Task: relocate these module files, and update the rest of the repository so everything still works.

- `arrow/factory.py` -> `arrow/build/factory.py`

Requirements:
- Every import of a moved module anywhere in the repository (library code and tests) must keep working from its new location. Update imports; do not leave compatibility stubs at the old paths.
- Do not delete, rename or weaken any test. The full test suite must still pass with the same number of passing tests as before you started (run it with `python -m pytest -q -o addopts=`).
- New package directories need an `__init__.py`.
- Do not commit. Work only inside this directory.

When finished, reply with one line saying what you moved.
