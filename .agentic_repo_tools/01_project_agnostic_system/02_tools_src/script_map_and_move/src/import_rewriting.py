"""Import rewriting - updating import statements during refactoring."""

from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from models import ImportInfo
from import_resolution import file_path_to_module, calculate_new_import_path
from import_parsing import find_importers


def find_module_string_references(file_path: Path, old_module: str,
                                  new_module: str) -> List[Tuple[int, str, str]]:
    """
    Find string references to a module in configuration files.

    Args:
        file_path: Path to file to search
        old_module: Old module path (e.g., 'src.math.add')
        new_module: New module path (e.g., 'src.utils.math.add')

    Returns:
        List of (line_number, old_line, new_line) tuples
    """
    changes = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception:
        return []

    for lineno, line in enumerate(lines, start=1):
        # Skip comments
        if line.strip().startswith('#'):
            continue

        # Look for module references in strings
        if old_module in line:
            # Simple string replacement
            new_line = line.replace(old_module, new_module)
            if new_line != line:
                changes.append((lineno, line.rstrip(), new_line.rstrip()))

    return changes


def apply_line_updates(file_path: Path, changes: List[Tuple[int, str, str]]) -> None:
    """
    Apply line-level updates to a file.

    Args:
        file_path: Path to file to update
        changes: List of (line_number, old_content, new_content) tuples
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Apply changes (reverse order to preserve line numbers)
    for lineno, old_content, new_content in sorted(changes, key=lambda x: x[0], reverse=True):
        idx = lineno - 1
        if idx < len(lines):
            lines[idx] = new_content + '\n'

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)


def rewrite_import_statement(original_import: ImportInfo,
                             new_module_path: str,
                             importing_file: Path,
                             root_dir: Path,
                             package_prefix: str = "") -> str:
    """
    Rewrite an import statement to point to new module location.

    Args:
        original_import: Original import info
        new_module_path: New absolute module path
        importing_file: File containing the import
        root_dir: Project root
        package_prefix: Package prefix for resolution

    Returns:
        New import statement as string
    """
    # Calculate new import path (handles relative vs absolute)
    new_import_path = calculate_new_import_path(
        original_import,
        new_module_path,
        importing_file,
        root_dir,
        package_prefix
    )

    # Build new import statement
    if original_import.names:
        # from X import Y
        if original_import.alias:
            return f"from {new_import_path} import {original_import.names[0]} as {original_import.alias}"
        else:
            return f"from {new_import_path} import {', '.join(original_import.names)}"
    else:
        # import X or import X as Y
        if original_import.alias:
            return f"import {new_import_path} as {original_import.alias}"
        else:
            return f"import {new_import_path}"


def rewrite_import_for_move(imp: ImportInfo, importing_file: Path,
                            old_path: Path, new_path: Path,
                            root_dir: Path, package_prefix: str = "") -> str:
    """
    Rewrite a single import to account for a file move.

    Args:
        imp: Import to rewrite
        importing_file: File containing the import
        old_path: Original file path
        new_path: New file path
        root_dir: Project root
        package_prefix: Package prefix for resolution

    Returns:
        New import statement
    """
    new_module = file_path_to_module(new_path, root_dir, package_prefix)

    # If relative import, calculate new relative path
    if imp.is_relative:
        # Get importing file's module path
        importing_module = file_path_to_module(importing_file, root_dir, package_prefix)
        importing_parts = importing_module.split('.')
        new_parts = new_module.split('.')

        # Calculate common prefix
        common_len = 0
        for i, (a, b) in enumerate(zip(importing_parts[:-1], new_parts)):
            if a == b:
                common_len = i + 1
            else:
                break

        # Calculate levels up needed
        levels_up = len(importing_parts) - 1 - common_len
        remaining = new_parts[common_len:]

        # Build relative import
        if levels_up == 0 and remaining:
            from_part = f".{'.'.join(remaining)}"
        elif levels_up == 0:
            from_part = "."
        else:
            dots = '.' * (levels_up + 1)
            if remaining:
                from_part = f"{dots}{'.'.join(remaining)}"
            else:
                from_part = dots

        # Combine with imported names
        if imp.names:
            if imp.alias:
                return f"from {from_part} import {imp.names[0]} as {imp.alias}"
            else:
                return f"from {from_part} import {', '.join(imp.names)}"
        else:
            # This shouldn't happen for relative imports but handle it
            return f"from {from_part}"
    else:
        # Absolute import - just use new module path
        if imp.names:
            if imp.alias:
                return f"from {new_module} import {imp.names[0]} as {imp.alias}"
            else:
                return f"from {new_module} import {', '.join(imp.names)}"
        else:
            if imp.alias:
                return f"import {new_module} as {imp.alias}"
            else:
                return f"import {new_module}"


def update_imports_in_file(file_path: Path, import_updates: List[Tuple[int, str, Optional[int]]]) -> None:
    """
    Update import statements in a file.

    Args:
        file_path: Path to file to update
        import_updates: List of (line_number, new_import_statement, end_line_number) tuples
                       end_line_number is None for single-line imports
    """
    # Read file
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Sort updates by line number (reverse order to avoid index shifting)
    updates_sorted = sorted(import_updates, key=lambda x: x[0], reverse=True)

    # Apply updates
    for lineno, new_statement, end_lineno in updates_sorted:
        # lineno is 1-indexed, list is 0-indexed
        start_idx = lineno - 1

        if start_idx < len(lines):
            # Preserve indentation from original first line
            original = lines[start_idx]
            indent = len(original) - len(original.lstrip())

            # Replace first line with new statement
            lines[start_idx] = ' ' * indent + new_statement + '\n'

            # If multiline import, delete continuation lines
            if end_lineno and end_lineno > lineno:
                # Delete lines from start_idx+1 to end_idx (inclusive)
                end_idx = end_lineno - 1
                num_lines_to_delete = end_idx - start_idx
                for _ in range(num_lines_to_delete):
                    if start_idx + 1 < len(lines):
                        del lines[start_idx + 1]

    # Write file back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)


def preview_import_changes(file_path: Path, import_updates: List[Tuple[int, str, str]]) -> None:
    """
    Preview changes without applying them.

    Args:
        file_path: Path to file
        import_updates: List of (line_number, old_statement, new_statement) tuples
    """
    print(f"\n{file_path}:")
    for lineno, old_stmt, new_stmt in sorted(import_updates, key=lambda x: x[0]):
        print(f"  Line {lineno}:")
        print(f"    - {old_stmt}")
        print(f"    + {new_stmt}")


def rewrite_imports_for_move(old_path: Path, new_path: Path,
                             dependency_map: Dict[Path, List[ImportInfo]],
                             root_dir: Path, dry_run: bool = False, package_prefix: str = "") -> Dict[Path, List[Tuple[int, str, Optional[int]]]]:
    """
    Find and rewrite all imports affected by moving a file.

    Args:
        old_path: Current file path
        new_path: New file path
        dependency_map: Complete dependency map
        root_dir: Project root
        dry_run: If True, show changes without applying
        package_prefix: Package prefix for resolution

    Returns:
        Dictionary mapping files to their import updates
    """
    old_module = file_path_to_module(old_path, root_dir, package_prefix)
    new_module = file_path_to_module(new_path, root_dir, package_prefix)

    print(f"\nRewriting imports: {old_module} -> {new_module}")

    updates = {}
    preview_data = {}

    # Find all files that import from old_path
    importers = find_importers(old_path, dependency_map, root_dir, package_prefix)

    for importing_file, relevant_imports in importers:
        file_updates = []
        file_previews = []

        # Group imports by line number to handle multi-import statements
        imports_by_line = defaultdict(list)
        for imp in relevant_imports:
            imports_by_line[imp.lineno].append(imp)

        for lineno, imps in imports_by_line.items():
            # If multiple imports on same line, combine them
            if len(imps) > 1:
                # Get the original line and new module
                raw_line = imps[0].raw_line
                new_module_path = file_path_to_module(new_path, root_dir, package_prefix)

                # Collect all imported names from this line
                all_names = []
                for imp in imps:
                    if imp.names:
                        all_names.extend(imp.names)

                # Build combined import statement
                if imps[0].is_relative:
                    # Handle relative imports
                    importing_module = file_path_to_module(importing_file, root_dir, package_prefix)
                    importing_parts = importing_module.split('.')
                    new_parts = new_module_path.split('.')

                    # Calculate relative path
                    common_len = 0
                    for i, (a, b) in enumerate(zip(importing_parts[:-1], new_parts)):
                        if a == b:
                            common_len = i + 1
                        else:
                            break

                    levels_up = len(importing_parts) - 1 - common_len
                    remaining = new_parts[common_len:]

                    if levels_up == 0 and remaining:
                        from_part = f"from .{'.'.join(remaining)}"
                    elif levels_up == 0:
                        from_part = "from ."
                    else:
                        dots = '.' * (levels_up + 1)
                        if remaining:
                            from_part = f"from {dots}{'.'.join(remaining)}"
                        else:
                            from_part = f"from {dots}"
                else:
                    from_part = f"from {new_module_path}"

                # Combine all names
                new_stmt = f"{from_part} import {', '.join(all_names)}"

                # Use end_lineno from first import in group (they should all have same end_lineno)
                end_lineno = imps[0].end_lineno
                file_updates.append((lineno, new_stmt, end_lineno))
                file_previews.append((lineno, raw_line, new_stmt))
            else:
                # Single import on this line
                imp = imps[0]
                new_stmt = rewrite_import_for_move(imp, importing_file, old_path, new_path, root_dir, package_prefix)

                file_updates.append((imp.lineno, new_stmt, imp.end_lineno))
                file_previews.append((imp.lineno, imp.raw_line, new_stmt))

        if file_updates:
            updates[importing_file] = file_updates
            preview_data[importing_file] = file_previews

    # Show preview
    if preview_data:
        print(f"\nWill update {len(preview_data)} file(s):")
        for file_path, previews in preview_data.items():
            preview_import_changes(file_path, previews)

    return updates
