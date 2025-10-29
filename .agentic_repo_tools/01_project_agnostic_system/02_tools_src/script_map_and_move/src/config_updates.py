"""Configuration file updates - updating module references in config files."""

from pathlib import Path
from typing import Dict, List, Tuple

from import_resolution import file_path_to_module
from import_rewriting import find_module_string_references, apply_line_updates


# Configuration file patterns to scan for string references
CONFIG_FILE_PATTERNS = [
    'setup.py',
    'setup.cfg',
    'pyproject.toml',
    'settings.py',
    'config.py',
    'celeryconfig.py',
    '*.ini',
    '*.cfg',
    '*.yaml',
    '*.yml',
    '*.toml',
    'pytest.ini',
    'tox.ini',
    '.flake8',
]


def update_config_files(old_path: Path, new_path: Path, root_dir: Path,
                       dry_run: bool = False, package_prefix: str = "") -> Dict[Path, List[Tuple[int, str, str]]]:
    """
    Update module string references in configuration files.

    Args:
        old_path: Old file path
        new_path: New file path
        root_dir: Project root
        dry_run: If True, only preview changes
        package_prefix: Package prefix for resolution

    Returns:
        Dictionary mapping files to their updates
    """
    old_module = file_path_to_module(old_path, root_dir, package_prefix)
    new_module = file_path_to_module(new_path, root_dir, package_prefix)

    all_updates = {}

    # Find all config files
    config_files = []
    for pattern in CONFIG_FILE_PATTERNS:
        config_files.extend(root_dir.glob(pattern))
        # Also search recursively for settings.py and config.py
        if pattern in ['settings.py', 'config.py']:
            config_files.extend(root_dir.glob(f'**/{pattern}'))

    # Deduplicate and filter
    config_files = list(set([f for f in config_files if f.is_file() and '.tools' not in str(f)]))

    if not config_files:
        return all_updates

    for config_file in config_files:
        try:
            changes = find_module_string_references(config_file, old_module, new_module)

            if changes:
                all_updates[config_file] = changes

                print(f"\n  {config_file.relative_to(root_dir)}:")
                for lineno, old_line, new_line in changes:
                    print(f"    Line {lineno}:")
                    print(f"      - {old_line}")
                    print(f"      + {new_line}")

                if not dry_run:
                    # Apply changes
                    apply_line_updates(config_file, changes)

        except Exception as e:
            print(f"  Warning: Could not process {config_file}: {e}")

    return all_updates
