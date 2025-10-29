# Known Limitations

## What This Tool Does NOT Handle

### 1. String-Based Imports

The tool only detects static import statements. Dynamic imports are not handled:

```python
# NOT DETECTED
module_name = "src.math.add"
mod = importlib.import_module(module_name)

# NOT DETECTED
exec("from src.math import add")
```

**Workaround:** Use static imports where possible.

### 2. Import Statements in Strings

Imports in comments, docstrings, or string literals are not updated:

```python
"""
Example usage:
    from src.math.add import add  # <-- NOT UPDATED
"""
```

**Workaround:** Update these manually after refactoring.

### 3. Circular Imports

The tool preserves circular imports as-is. It does not detect or break circular dependencies.

```python
# file1.py imports file2.py
# file2.py imports file1.py
# Both will be updated, but circular dependency remains
```

**Workaround:** Refactor code to eliminate circular dependencies before or after using the tool.

### 4. Star Imports

While star imports are detected, they may not work correctly after refactoring if the target module's structure changes:

```python
from src.math import *  # What gets imported?
```

**Workaround:** Use explicit imports instead of star imports.

### 5. Non-Python Files

Only `.py` files are processed. Other files that might reference Python modules are not updated:

- Configuration files (`.yaml`, `.toml`, `.ini`)
- Documentation (`.md`, `.rst`)
- Shell scripts
- Test fixtures

**Workaround:** Manually update these files after refactoring.

### 6. External Package References

If your code references file paths as strings (e.g., in configuration), these are not updated:

```python
CONFIG = {
    "module_path": "src/math/add.py"  # <-- NOT UPDATED
}
```

**Workaround:** Update these manually.

### 7. Namespace Packages

The tool assumes standard package structure with `__init__.py` files. PEP 420 namespace packages (without `__init__.py`) may not work correctly.

**Workaround:** Use traditional packages with `__init__.py`.

### 8. Moving Entire Directories

Currently, you must specify each file individually. Moving entire directories with one entry is not supported.

**Workaround:** List all files in the directory in your refactor plan, or add this as a future enhancement.

## Edge Cases That ARE Handled

✓ Empty files
✓ Files with no imports
✓ `__init__.py` files
✓ Files with syntax errors (skipped with warning)
✓ Deeply nested directory structures
✓ Mixed absolute and relative imports
✓ Aliased imports

## Performance Limitations

- Tested on projects with up to ~200 files
- Large projects (1000+ files) may be slow
- No parallelization of file processing

## Future Improvements

See `sprint_plan.md` under "Future Enhancements" for planned features that would address some of these limitations.
