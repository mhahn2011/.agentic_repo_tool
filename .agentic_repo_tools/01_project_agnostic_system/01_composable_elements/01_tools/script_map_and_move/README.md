# Script Map and Move

**Purpose:** Safely move Python files while automatically updating all import statements and configuration references across the codebase.

**Status:** ✅ Production ready

## Features

- **Dependency Mapping:** Discovers and maps all import relationships using AST parsing
- **Safe File Moving:** Validates operations before execution
- **Automatic Import Updates:** Rewrites all import statements (absolute, relative, multiline, aliased)
- **Configuration Updates:** Updates module references in setup.py, pyproject.toml, etc.
- **Git Integration:** Creates checkpoints with automatic rollback support
- **Validation:** Verifies no broken imports remain after refactoring

## Usage

### From Tool Directory

```bash
# Navigate to the tool
cd .agentic_repo_tools/01_project_agnostic_system/01_composable_elements/01_tools/script_map_and_move

# Run with dry-run to preview changes
python3 cli/refactor_tool.py --plan /path/to/your/refactor_plan.json --dry-run

# Execute refactoring
python3 cli/refactor_tool.py --plan /path/to/your/refactor_plan.json
```

### From Project Root

```bash
# Run directly from project root
python3 .agentic_repo_tools/01_project_agnostic_system/01_composable_elements/01_tools/script_map_and_move/cli/refactor_tool.py \
  --plan refactor_plan.json \
  --root .
```

## Inputs

### Required

- **Refactor Plan (JSON file):** Specifies which files to move

**Recommended location:** Create your refactor plan in the project-specific data directory:
```
../../../../../../02_project_specific_data/01_composable_elements/01_tools/script_map_and_move/my_refactor_plan.json
```

**Format:**
```json
{
  "moves": [
    {
      "from": "src/old_location/module.py",
      "to": "src/new_location/module.py"
    }
  ]
}
```

**Example files:** See `examples/` folder for sample refactor plans:
- `refactor_plan.example.json` - Basic file moves
- `refactor_plan_reverse.example.json` - Reverse refactoring
- `refactor_registry.example.json` - Registry-based configuration

Copy an example to the `02_project_specific_data/` directory and customize it for your project.

### Optional

- `--root DIR` - Project root directory (defaults to current directory)
- `--dry-run` - Preview changes without applying them
- `--verify-only` - Validate plan without executing
- `--no-commit` - Skip git commit operations
- `--yes` / `-y` - Skip interactive prompts (for CI/automation)

## Outputs

**All outputs are automatically saved to:**
```
../../../../../../02_project_specific_data/01_composable_elements/01_tools/script_map_and_move/
```

### Generated Files

**Registry files** (when using `--init-registry` or `--generate-registry`):
- `refactor_registry.json` - JSON mapping of file locations (created with `--init-registry`)
- `refactor_registry.py` - Python module with import exports (created with `--generate-registry`)

**Reports and logs** (planned features):
- `refactor_report_YYYY-MM-DD.md` - Summary of files moved and changes made
- `import_updates.log` - Detailed log of import statement changes

**Git commits** (if `--no-commit` not used):
  - Pre-refactor checkpoint
  - Post-refactor commit with detailed change summary

## Dependencies

### Required

- **Python 3.6+**
- **Standard library only** (no external packages)

Standard library modules used:
- `ast` - Abstract Syntax Trees for import parsing
- `pathlib`, `os`, `shutil` - File operations
- `json` - Configuration parsing
- `subprocess` - Git integration
- `argparse` - CLI
- `collections`, `typing` - Data structures

### Optional

- **Git** - For checkpoint/rollback features (optional but recommended)

## CLI Entry Points

Main command:
```bash
python3 cli/refactor_tool.py [OPTIONS]
```

**Required Options:**
- `--plan FILE` - Path to refactor plan JSON

**Optional Flags:**
- `--dry-run` - Preview changes without applying
- `--verify-only` - Validate plan without executing
- `--no-commit` - Skip git operations
- `--yes` / `-y` - Non-interactive mode
- `--root DIR` - Project root (default: current directory)
- `--init-registry` - Generate import registry from current structure

## Import Patterns Supported

- **Absolute:** `from src.module import function`
- **Relative:** `from .module import function` / `from ..sibling import Class`
- **Module:** `import src.module` / `import src.module as sm`
- **Aliased:** `from src.module import function as fn`
- **Multiline:** Handles imports spanning multiple lines
- **Module usage in code:** Updates `module.function()` references

## Architecture

**Tool Structure (in `01_project_agnostic_system`):**
```
script_map_and_move/
├── cli/
│   └── refactor_tool.py          # Main entry point
├── src/
│   ├── models.py                 # Data structures (ImportInfo)
│   ├── file_operations.py        # File moving and __init__ creation
│   ├── import_parsing.py         # AST-based dependency mapping
│   ├── import_resolution.py      # Module path conversions
│   ├── import_rewriting.py       # Import statement updates
│   ├── config_updates.py         # Configuration file updates
│   ├── validation.py             # Safety checks
│   ├── git_integration.py        # Version control operations
│   ├── orchestration.py          # High-level workflows
│   └── registry_mode.py          # Registry-based refactoring
├── examples/
│   ├── refactor_plan.example.json          # Example: basic file moves
│   ├── refactor_plan_reverse.example.json  # Example: reverse refactoring
│   └── refactor_registry.example.json      # Example: registry-based config
├── README.md                     # This file
└── LIMITATIONS.md                # Known limitations

Total: ~2,700 lines of modular, maintainable code
```

**Project-Specific Data (in `02_project_specific_data`):**
```
script_map_and_move/
└── (user-created refactor plans and tool-generated outputs appear here at runtime)
```

## Tested On

Successfully validated on real-world Python projects:
- **arrow** (21 files, 251 imports) - Date/time library
- **httpie** (133 files, 1340 imports) - HTTP CLI client
- **rich** (190 files, 1859 imports) - Terminal formatting library

See `../../../../../TEST_RESULTS.md` for detailed validation results.

## Safety Features

- **Pre-flight validation:** Verifies all file operations before execution
- **Import verification:** Checks imports before and after refactoring
- **Dry-run mode:** Preview all changes safely
- **Git checkpoints:** Automatic snapshots with rollback instructions
- **Dynamic import detection:** Warns about string-based imports that can't be auto-updated
- **Clear error messages:** Detailed feedback for troubleshooting

## Example Workflow

```bash
# 1. Create a refactor plan
cat > refactor_plan.json <<EOF
{
  "moves": [
    {
      "from": "myproject/utils.py",
      "to": "myproject/core/utils.py"
    }
  ]
}
EOF

# 2. Preview changes (dry run)
python3 cli/refactor_tool.py --plan refactor_plan.json --root /path/to/project --dry-run

# 3. Execute refactoring
python3 cli/refactor_tool.py --plan refactor_plan.json --root /path/to/project

# 4. Review outputs
ls ../../../../../../02_project_specific_data/01_composable_elements/01_tools/script_map_and_move/

# 5. If needed, rollback using git
cd /path/to/project
git log  # Find pre-refactor commit
git reset --hard <commit-hash>
```

## Limitations

See `LIMITATIONS.md` for known limitations, including:
- String-based dynamic imports not detected (`__import__`, `importlib.import_module`)
- Circular imports preserved as-is (not automatically resolved)
- Non-Python files not scanned or updated
- Import statements in comments or strings not updated

## Usage Pattern

This tool is typically used:
- **After code is functionally complete** - reorganizing without changing behavior
- **During cleanup and refactoring** - improving code structure and maintainability
- **For large-scale reorganizations** - moving multiple files while preserving imports
- **When restructuring packages** - safely updating module hierarchies

---

**Tool Status:** Production ready • Extensively tested • Zero external dependencies
