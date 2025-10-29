"""Import resolution - converting between file paths and module names."""

import os
from pathlib import Path
from typing import Optional

from models import ImportInfo


def file_path_to_module(file_path: Path, root_dir: Path, package_prefix: str = "") -> str:
    """
    Convert file path to Python module path.
    e.g., src/math/add.py -> src.math.add
    """
    if package_prefix:
        try:
            relative = file_path.relative_to(root_dir / package_prefix)
        except ValueError:
            relative = file_path.relative_to(root_dir)
    else:
        relative = file_path.relative_to(root_dir)

    if relative.name == "__init__.py":
        parts = relative.parent.parts
    else:
        parts = relative.with_suffix("").parts

    module_name = ".".join(parts)

    if package_prefix and not module_name.startswith(package_prefix):
        return f"{package_prefix}.{module_name}"

    return module_name


def module_to_file_path(module_name: str, root_dir: Path, package_prefix: str) -> Optional[Path]:
    """
    Convert a module name to a file path.
    e.g., "src.math.add" -> src/math/add.py
    """
    if package_prefix and module_name.startswith(package_prefix + "."):
        module_name = module_name[len(package_prefix)+1:]

    relative_path = Path(module_name.replace(".", os.sep))

    # Check for .py file
    file_path = root_dir / package_prefix / (str(relative_path) + ".py")
    if file_path.is_file():
        return file_path

    # Check for package
    dir_path = root_dir / package_prefix / relative_path / "__init__.py"
    if dir_path.is_file():
        return dir_path

    return None


def resolve_relative_import(imp: ImportInfo, importing_file: Path,
                            root_dir: Path, package_prefix: str = "") -> str:
    """
    Resolve relative import to absolute module path.

    Args:
        imp: ImportInfo with relative import
        importing_file: File containing the import
        root_dir: Project root
        package_prefix: Package prefix for resolution

    Returns:
        Absolute module path
    """
    # Get the importing file's package
    importing_module = file_path_to_module(importing_file, root_dir, package_prefix)
    parts = importing_module.split('.')

    # Go up 'level' directories
    # level=1 means current package, level=2 means parent, etc.
    parts = parts[:-imp.level] if imp.level > 0 else parts[:-1]

    # Add the imported module
    if imp.module:
        parts.append(imp.module)

    return '.'.join(parts)


def calculate_new_import_path(old_file_path: Path, new_file_path: Path,
                               importing_file: Path, root_dir: Path,
                               use_relative: bool = False) -> str:
    """
    Calculate what the new import path should be after file moves.

    Args:
        old_file_path: Current location of file being imported
        new_file_path: Future location of file being imported
        importing_file: File that contains the import statement
        root_dir: Project root directory
        use_relative: Whether to generate relative import

    Returns:
        New import module path (e.g., 'src.core.math.add' or '.core.math.add')
    """
    new_module = file_path_to_module(new_file_path, root_dir)

    if not use_relative:
        return new_module

    # Calculate relative path
    importing_module = file_path_to_module(importing_file, root_dir)
    importing_parts = importing_module.split('.')
    new_parts = new_module.split('.')

    # Find common prefix
    common_len = 0
    for i, (a, b) in enumerate(zip(importing_parts, new_parts)):
        if a == b:
            common_len = i + 1
        else:
            break

    # Calculate levels up needed
    # If importing from src/main.py, we're at level 1 (src)
    # To import from src/core/math/add.py, we go up 0 levels
    levels_up = len(importing_parts) - common_len

    # Remaining path after common prefix
    remaining = new_parts[common_len:]

    # Build relative import
    if levels_up == 0:
        # Same package
        prefix = '.'
    else:
        prefix = '.' * (levels_up + 1)

    if remaining:
        return prefix + '.'.join(remaining)
    else:
        return prefix
