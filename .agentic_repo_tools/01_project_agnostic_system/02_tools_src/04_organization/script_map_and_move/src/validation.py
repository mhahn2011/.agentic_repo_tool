"""Validation functions - verifying refactor operations and import integrity."""

from pathlib import Path
from typing import List, Tuple

from import_parsing import build_dependency_map
from import_resolution import module_to_file_path


def verify_no_broken_imports(root_dir: Path, package_prefix: str = "") -> Tuple[bool, List[str]]:
    """
    Verify that all import statements can be resolved.

    Args:
        root_dir: Project root directory
        package_prefix: Package prefix for resolution

    Returns:
        Tuple of (all_valid, list_of_errors)
    """
    errors = []

    # Build dependency map
    dep_map = build_dependency_map(root_dir, package_prefix)

    # Check each import
    for file_path, imports in dep_map.items():
        for imp in imports:
            # Skip external imports (not resolvable to project files)
            if not imp.module:
                continue

            # Try to resolve to a file
            try:
                resolved = module_to_file_path(imp.module, root_dir, package_prefix)
                if resolved and not resolved.exists():
                    rel_path = file_path.relative_to(root_dir)
                    errors.append(f"{rel_path}:{imp.lineno} - Cannot resolve: {imp.raw_line}")
            except Exception:
                # External or unresolvable import - that's okay
                pass

    return (len(errors) == 0, errors)


def verify_file_operations(moves: List[Tuple[Path, Path]], root_dir: Path) -> Tuple[bool, List[str]]:
    """
    Verify that all file operations are valid.

    Args:
        moves: List of (old_path, new_path) tuples
        root_dir: Project root

    Returns:
        Tuple of (all_valid, list_of_errors)
    """
    errors = []

    for old_path, new_path in moves:
        # Check source exists
        if not old_path.exists():
            errors.append(f"Source file does not exist: {old_path.relative_to(root_dir)}")

        # Check destination doesn't already exist
        if new_path.exists():
            errors.append(f"Destination already exists: {new_path.relative_to(root_dir)}")

        # Check source is within root
        try:
            old_path.relative_to(root_dir)
        except ValueError:
            errors.append(f"Source file is outside project root: {old_path}")

        # Check destination is within root
        try:
            new_path.relative_to(root_dir)
        except ValueError:
            errors.append(f"Destination is outside project root: {new_path}")

    return (len(errors) == 0, errors)
