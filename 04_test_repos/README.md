# Test Repositories

This directory contains sample repositories for testing toolkit tools.

## Structure

Each test repo has two subdirectories:

```
04_test_repos/
├── <repo_name>/
│   ├── 01_original/        # Pristine copy (never modify)
│   └── 02_modified/        # Working copy for running tests
```

## Usage

**Setup:**
1. Clone or copy a test repository into `01_original/`
2. Copy `01_original/` to `02_modified/` when running tests

**Testing workflow:**
```bash
# Reset to pristine state
rm -rf 04_test_repos/arrow/02_modified/*
cp -r 04_test_repos/arrow/01_original/* 04_test_repos/arrow/02_modified/

# Run tool tests on 02_modified/
.agentic_repo_tools/01_project_agnostic_system/01_composable_elements/01_tools/script_map_and_move/cli/refactor_tool.py \
  --project 04_test_repos/arrow/02_modified/

# Inspect results, compare to original
diff -r 04_test_repos/arrow/01_original/ 04_test_repos/arrow/02_modified/
```

## Available Test Repos

### arrow/
Python datetime library with complex import structure
- **Size:** ~23 Python files, 251 imports
- **Good for:** Testing refactoring, import rewriting
- **Source:** https://github.com/arrow-py/arrow

## Adding New Test Repos

1. Create directory: `mkdir -p 04_test_repos/<repo_name>/{01_original,02_modified}`
2. Clone into `01_original/`: `git clone <url> 04_test_repos/<repo_name>/01_original`
3. Document in this README
4. **Important:** Test repos are gitignored - they won't be committed to this repo

## Notes

- All test repos are gitignored (see root `.gitignore`)
- Keep `01_original/` pristine - never run tools directly on it
- Always work in `02_modified/` copies
- Reset `02_modified/` before each test run for consistency
