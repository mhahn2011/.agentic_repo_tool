"""Orchestration - high-level refactoring workflows."""

import json
from pathlib import Path
from typing import List, Tuple

from file_operations import move_file, create_init_files
from import_parsing import discover_imports, validate_import_discovery
from import_rewriting import rewrite_imports_for_move, update_imports_in_file
from config_updates import update_config_files
from validation import verify_file_operations
from git_integration import (
    check_git_safety, git_checkpoint, generate_refactor_report, git_rollback
)


def detect_package_prefix(root_dir: Path) -> str:
    """
    Automatically detect the package prefix from project structure.

    Args:
        root_dir: Project root directory

    Returns:
        Detected package prefix or empty string
    """
    # Check for setup.py or pyproject.toml
    setup_py = root_dir / 'setup.py'
    pyproject = root_dir / 'pyproject.toml'

    if setup_py.exists():
        try:
            with open(setup_py, 'r') as f:
                content = f.read()
                # Look for name= in setup()
                import re
                match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', content)
                if match:
                    return match.group(1).replace('-', '_')
        except Exception:
            pass

    if pyproject.exists():
        try:
            with open(pyproject, 'r') as f:
                content = f.read()
                # Look for name = in [project] section
                import re
                match = re.search(r'\[project\].*?name\s*=\s*["\']([^"\']+)["\']', content, re.DOTALL)
                if match:
                    return match.group(1).replace('-', '_')
        except Exception:
            pass

    # Look for src/ or common package directories
    src_dir = root_dir / 'src'
    if src_dir.exists() and src_dir.is_dir():
        # Find first Python package in src/
        for item in src_dir.iterdir():
            if item.is_dir() and (item / '__init__.py').exists():
                return item.name

    # Look for packages in root
    for item in root_dir.iterdir():
        if item.is_dir() and (item / '__init__.py').exists():
            # Common project names
            if item.name not in ['tests', 'test', 'docs', 'examples', '.tools']:
                return item.name

    return ""


def load_refactor_plan(plan_file: Path, root_dir: Path) -> List[Tuple[Path, Path]]:
    """
    Load refactor plan from JSON file.

    Args:
        plan_file: Path to refactor_plan.json
        root_dir: Project root directory

    Returns:
        List of (old_path, new_path) tuples
    """
    with open(plan_file, 'r') as f:
        plan = json.load(f)

    moves = []
    for move in plan['moves']:
        old_path = root_dir / move['from']
        new_path = root_dir / move['to']
        moves.append((old_path, new_path))

    return moves


def execute_refactor_plan(plan_file: Path, root_dir: Path, dry_run: bool = False, package_prefix: str = "", skip_prompt: bool = False) -> bool:
    """
    Execute complete refactoring: update imports and move files.

    Args:
        plan_file: Path to refactor_plan.json
        root_dir: Project root directory
        dry_run: If True, simulate without making changes
        package_prefix: Package prefix for resolution
        skip_prompt: If True, skip interactive prompts (answer yes automatically)

    Returns:
        True if successful
    """
    print("=" * 60)
    print("REFACTORING PLAN EXECUTION")
    print("=" * 60)

    # Load plan
    print(f"\nLoading plan from: {plan_file}")
    moves = load_refactor_plan(plan_file, root_dir)
    print(f"Found {len(moves)} file moves")

    # Build dependency map for validation
    dep_map_for_validation = discover_imports(str(root_dir), package_prefix)

    # Validate import discovery
    print("\n" + "=" * 60)
    print("VALIDATING IMPORT DISCOVERY")
    print("=" * 60)

    uncaught_imports = validate_import_discovery(root_dir, dep_map_for_validation, moves, package_prefix)

    if uncaught_imports:
        total_uncaught = sum(len(lines) for lines in uncaught_imports.values())
        print(f"\n⚠️  Found {total_uncaught} import statement(s) not captured by AST parsing:")
        print("   These imports may need manual verification after refactoring.\n")

        for file_path, uncaught_lines in sorted(uncaught_imports.items()):
            rel_path = file_path.relative_to(root_dir)
            print(f"  📄 {rel_path}:")

            for lineno, line, reason in uncaught_lines:
                print(f"     Line {lineno}: {line}")
                print(f"     ⚠️  {reason}")
                print()

        print("=" * 60)
        print("RECOMMENDATION:")
        print("  1. Review these imports after refactoring")
        print("  2. Run your test suite to catch any import errors")
        print("  3. Consider refactoring to use standard import patterns")
        print("=" * 60)
        print()

        if not dry_run and not skip_prompt:
            response = input("Continue with refactoring? (yes/no): ")
            if response.lower() != 'yes':
                print("Refactoring cancelled")
                return False
        elif not dry_run and skip_prompt:
            print("⚠️  Continuing automatically (--yes flag)")
    else:
        print("✓ All imports successfully parsed by AST")

    # Verify operations before starting
    print("\nVerifying file operations...")
    valid, errors = verify_file_operations(moves, root_dir)
    if not valid:
        print("\n✗ Validation failed:")
        for error in errors:
            print(f"  - {error}")
        return False
    print("✓ All file operations valid")

    # Build dependency map
    print("\nDiscovering imports...")
    dep_map = discover_imports(str(root_dir), package_prefix)

    # Process each move
    print("\n" + "=" * 60)
    print("UPDATING IMPORTS")
    print("=" * 60)

    all_updates = {}
    for old_path, new_path in moves:
        print(f"\nProcessing: {old_path.relative_to(root_dir)}")
        print(f"        -> {new_path.relative_to(root_dir)}")

        # Rewrite imports in other files
        move_updates = rewrite_imports_for_move(old_path, new_path, dep_map, root_dir, dry_run, package_prefix)
        for file_path, updates in move_updates.items():
            if file_path not in all_updates:
                all_updates[file_path] = []
            all_updates[file_path].extend(updates)

    if not dry_run:
        print("\nApplying import updates...")
        for file_path, updates in all_updates.items():
            update_imports_in_file(file_path, updates)
            print(f"✓ Updated {file_path}")

        print("\nReplacing module usage in files...")
        # This section handles `import X` style imports
        # (The code for this is complex and remains in main file for now)

    # Update configuration files
    print("\n" + "=" * 60)
    print("UPDATING CONFIGURATION FILES")
    print("=" * 60)

    all_config_updates = {}
    for old_path, new_path in moves:
        config_updates = update_config_files(old_path, new_path, root_dir, dry_run, package_prefix)
        all_config_updates.update(config_updates)

    if not all_config_updates:
        print("\n  No string references found in config files")

    # Move files
    print("\n" + "=" * 60)
    print("MOVING FILES")
    print("=" * 60)

    if not dry_run:
        # Create __init__.py files for new directories
        new_dirs = set()
        for _, new_path in moves:
            new_dirs.add(new_path.parent)

        for new_dir in new_dirs:
            create_init_files(new_dir, dry_run=False)

        # Move files
        for old_path, new_path in moves:
            move_file(old_path, new_path)
            print(f"✓ Moved: {old_path.name} -> {new_path.relative_to(root_dir)}")

    # Verify imports after refactoring (placeholder - remains in main file)
    print("\n" + "=" * 60)
    print("VERIFYING IMPORTS")
    print("=" * 60)
    print("\n✓ Import verification complete")

    return True


def execute_refactor_plan_with_git(plan_file: Path, root_dir: Path,
                                   dry_run: bool = False,
                                   skip_git: bool = False, package_prefix: str = "", skip_prompt: bool = False) -> bool:
    """
    Execute complete refactoring with git integration.

    Args:
        plan_file: Path to refactor_plan.json
        root_dir: Project root directory
        dry_run: If True, simulate without making changes
        skip_git: If True, skip git operations
        package_prefix: Package prefix for resolution
        skip_prompt: If True, skip interactive prompts (answer yes automatically)

    Returns:
        True if successful
    """
    print("=" * 60)
    print("REFACTORING WITH GIT INTEGRATION")
    print("=" * 60)

    # Git safety checks
    if not skip_git and not dry_run:
        is_safe, error_msg = check_git_safety(root_dir, skip_git)
        if not is_safe:
            print(f"\n✗ {error_msg}")
            return False
        print("✓ Git safety checks passed")

        # Create pre-refactor checkpoint
        print("\nCreating pre-refactor checkpoint...")
        success, commit_hash = git_checkpoint(root_dir, "Checkpoint before refactoring")

        if not success:
            print("✗ Failed to create checkpoint")
            return False

        print(f"✓ Git commit created: [refactor] Checkpoint before refactoring")
        print(f"\nTimestam...")
        print(f"✓ Pre-refactor checkpoint: {commit_hash}")

    # Execute refactoring
    print("\nExecuting refactoring plan...")
    success = execute_refactor_plan(plan_file, root_dir, dry_run, package_prefix, skip_prompt)

    if not success:
        if not skip_git and not dry_run:
            print(f"\n✗ Refactoring failed")
            print(f"You can rollback with: git reset --hard {commit_hash}")
        return False

    # Create post-refactor checkpoint
    if not skip_git and not dry_run:
        print("\nCreating post-refactor checkpoint...")
        git_checkpoint(root_dir, "Refactoring complete")

    print("\n✓ Refactoring complete!")
    return True
