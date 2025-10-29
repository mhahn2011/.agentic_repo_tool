#!/usr/bin/env python3
"""
Safe file moving tool with automatic import rewriting.
"""

import ast
import os
import sys
import shutil
import json
import subprocess
import argparse
import importlib.util
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from models import ImportInfo
from file_operations import find_python_files, move_file, create_init_files
from import_resolution import (
    file_path_to_module, module_to_file_path, resolve_relative_import, calculate_new_import_path
)
from import_parsing import (
    parse_imports, find_text_based_imports, classify_uncaught_import,
    validate_import_discovery, build_dependency_map, find_importers, discover_imports
)


# Import all functions from modules
from import_rewriting import (
    find_module_string_references, apply_line_updates, rewrite_import_statement,
    rewrite_import_for_move, update_imports_in_file, preview_import_changes,
    rewrite_imports_for_move
)
from config_updates import update_config_files, CONFIG_FILE_PATTERNS
from validation import verify_no_broken_imports, verify_file_operations
from git_integration import (
    is_git_repo, get_git_status, has_uncommitted_changes, git_commit,
    get_current_commit_hash, git_checkpoint, check_git_safety, git_rollback,
    generate_refactor_report
)
from orchestration import (
    detect_package_prefix, load_refactor_plan, execute_refactor_plan,
    execute_refactor_plan_with_git
)
from registry_mode import (
    initialize_registry, verify_refactor_plan, generate_import_registry,
    update_registry_for_move, convert_imports_to_registry, convert_project_to_registry,
    execute_refactor_with_registry, should_use_registry_mode, validate_registry_conversion,
    check_auto_convert_safety, execute_refactor_with_auto_registry
)


def get_project_data_path() -> Path:
    """
    Get the path to 02_project_specific_data for this tool.

    Returns absolute path to the project-specific data directory.
    """
    # Tool is at: .agentic_repo_tools/01_project_agnostic_system/02_tools_src/04_organization/script_map_and_move/cli/refactor_tool.py
    # Target is:  .agentic_repo_tools/02_project_specific_data/04_organization/script_map_and_move/
    tool_file = Path(__file__).resolve()  # Get absolute path
    # Navigate: cli/ -> script_map_and_move/ -> 04_organization/ -> 02_tools_src/ -> 01_project_agnostic_system/ -> .agentic_repo_tools/
    agentic_root = tool_file.parent.parent.parent.parent.parent.parent
    data_path = agentic_root / "02_project_specific_data" / "04_organization" / "script_map_and_move"

    # Create directory if it doesn't exist
    data_path.mkdir(parents=True, exist_ok=True)

    return data_path


def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Safe file moving tool with automatic import rewriting',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Dry run (preview changes)
  %(prog)s --plan refactor_plan.json --dry-run

  # Execute refactoring with git commits
  %(prog)s --plan refactor_plan.json

  # Execute without git commits
  %(prog)s --plan refactor_plan.json --no-commit

  # Verify only (check for issues)
  %(prog)s --plan refactor_plan.json --verify-only
        '''
    )

    parser.add_argument(
        '--plan',
        type=str,
        required=False,
        help='Path to refactor plan JSON file'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without applying them'
    )

    parser.add_argument(
        '--no-commit',
        action='store_true',
        help='Skip git commit operations'
    )

    parser.add_argument(
        '--verify-only',
        action='store_true',
        help='Only verify the plan, do not execute'
    )

    parser.add_argument(
        '--init-registry',
        action='store_true',
        help='Initialize refactor registry from current structure'
    )

    parser.add_argument(
        '--generate-registry',
        action='store_true',
        help='Generate refactor_registry.py from current code'
    )

    parser.add_argument(
        '--convert-to-registry',
        action='store_true',
        help='Convert all imports to use registry (one-time operation)'
    )

    parser.add_argument(
        '--use-registry',
        action='store_true',
        help='Use registry-based refactoring (only update registry file)'
    )

    parser.add_argument(
        '--auto-convert-registry',
        action='store_true',
        help='Automatically convert to registry before refactoring (one-time setup + refactor)'
    )

    parser.add_argument(
        '--package-prefix',
        type=str,
        help='Override auto-detected package prefix (e.g., "src", "myapp")'
    )

    parser.add_argument(
        '--root',
        type=str,
        default='.',
        help='Project root directory (default: current directory)'
    )

    parser.add_argument(
        '--yes', '-y',
        action='store_true',
        help='Answer yes to all prompts (non-interactive mode)'
    )

    return parser.parse_args()

def main():

    """
    Main entry point for the refactoring tool.
    """
    args = parse_arguments()

    # Resolve paths
    root_dir = Path(args.root).resolve()

    # Validate inputs
    if not root_dir.exists():
        print(f"✗ Error: Root directory does not exist: {root_dir}")
        return 1

    # Detect package prefix
    if args.package_prefix:
        package_prefix = args.package_prefix
        print(f"✓ Using specified package prefix: {package_prefix}")
    else:
        package_prefix = detect_package_prefix(root_dir)
        if package_prefix:
            print(f"✓ Detected package prefix: {package_prefix}")
        else:
            print("✓ No package prefix detected.")

    # Handle --generate-registry
    if args.generate_registry:
        data_path = get_project_data_path()
        registry_file = data_path / "refactor_registry.py"
        generate_import_registry(root_dir, output_file=registry_file, package_prefix=package_prefix)
        print(f"✓ Registry module saved to: {registry_file}")
        return 0

    # Handle --convert-to-registry
    if args.convert_to_registry:
        print("\nWARNING: This will rewrite imports across your entire project.")
        print("Make sure you have committed all changes first.")
        response = input("\nContinue? (yes/no): ")

        if response.lower() != 'yes':
            print("Cancelled")
            return 0

        # Convert project
        convert_project_to_registry(root_dir, dry_run=False, package_prefix=package_prefix)

        print("\n✓ Conversion complete")
        print("\nNext steps:")
        print("1. Test that your code still works")
        print("2. Run your test suite")
        print("3. Commit the changes")
        print("4. Future refactors: use --use-registry flag")

        return 0

    # Handle --init-registry
    if args.init_registry:
        data_path = get_project_data_path()
        registry_file = data_path / "refactor_registry.json"
        initialize_registry(root_dir, output_file=registry_file)
        print(f"✓ Registry saved to: {registry_file}")
        return 0

    # Execute refactoring
    try:
        if args.plan:
            plan_file = Path(args.plan).resolve()

            if not plan_file.exists():
                print(f"✗ Plan file not found: {plan_file}")
                return 1

            # NEW: Auto-convert mode
            if args.auto_convert_registry:
                success = execute_refactor_with_auto_registry(
                    plan_file=plan_file,
                    root_dir=root_dir,
                    dry_run=args.dry_run,
                    skip_git=args.no_commit,
                    package_prefix=package_prefix
                )
            # Registry mode (already converted)
            elif args.use_registry:
                success = execute_refactor_with_registry(
                    plan_file=plan_file,
                    root_dir=root_dir,
                    dry_run=args.dry_run,
                    skip_git=args.no_commit,
                    package_prefix=package_prefix
                )
            # Direct mode (no registry)
            else:
                success = execute_refactor_plan_with_git(
                    plan_file=plan_file,
                    root_dir=root_dir,
                    dry_run=args.dry_run,
                    skip_git=args.no_commit,
                    package_prefix=package_prefix,
                    skip_prompt=args.yes
                )
            return 0 if success else 1
        elif args.verify_only:
            if not args.plan:
                print("✗ Error: --verify-only requires a --plan file.")
                return 1
            plan_file = Path(args.plan).resolve()
            if not plan_file.exists():
                print(f"✗ Plan file not found: {plan_file}")
                return 1
            success = verify_refactor_plan(plan_file, root_dir, package_prefix)
            return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n\n✗ Interrupted by user")
        return 130

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
