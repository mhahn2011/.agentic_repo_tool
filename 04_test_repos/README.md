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

**Quick Reset (Recommended):**
```bash
# Reset all test repos with latest toolkit
cd 04_test_repos
./reset_tests.sh

# Or reset specific repo
./reset_tests.sh arrow
```

**Manual Testing workflow:**
```bash
# Run tool tests on 02_modified/ (toolkit already inside)
cd 04_test_repos/arrow/02_modified
.agentic_repo_tools/01_project_agnostic_system/01_composable_elements/01_tools/script_map_and_move/cli/refactor_tool.py \
  <args>

# Inspect results, compare to original
diff -r ../01_original/ .
```

## Reset Script

**`reset_tests.sh`** prepares test repos for fresh testing:
- Deletes all `02_modified/` contents
- Copies fresh `01_original/` to `02_modified/`
- Copies latest `.agentic_repo_tools/` into each `02_modified/`

**Usage:**
```bash
./reset_tests.sh           # Reset all repos
./reset_tests.sh arrow     # Reset specific repo
```

Run this before each major test cycle to ensure clean state and latest toolkit version.

## Available Test Repos

### arrow/
Python datetime library with complex import structure
- **Size:** ~23 Python files, 251 imports
- **Good for:** Testing refactoring, import rewriting
- **Source:** https://github.com/arrow-py/arrow

### click/
Python CLI creation library
- **Size:** Large codebase with extensive CLI utilities
- **Good for:** Testing complex codebases, CLI tool refactoring
- **Source:** https://github.com/pallets/click

### example_app/
Small example application (local, no public repo)
- **Size:** Small Python application
- **Good for:** Quick testing, validating basic functionality

### httpie/
Modern command-line HTTP client
- **Size:** ~133 Python files (large codebase)
- **Good for:** Testing large-scale refactoring
- **Source:** https://github.com/httpie/cli

### pycalculator/
Simple Python calculator
- **Size:** Small, focused codebase
- **Good for:** Simple refactoring tests, quick validation
- **Source:** https://github.com/juliotrigo/pycalculator

### rich/
Python library for rich text and formatting in terminal
- **Size:** ~190 Python files (very large codebase)
- **Good for:** Stress testing, large-scale import management
- **Source:** https://github.com/Textualize/rich

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
