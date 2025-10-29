"""File system operations for the refactor tool."""

import shutil
from pathlib import Path
from typing import List


def find_python_files(root_dir: Path) -> List[Path]:
    """
    Recursively find all .py files in directory.

    Args:
        root_dir: Root directory to scan

    Returns:
        List of Path objects for all .py files
    """
    python_files = []

    for path in root_dir.rglob("*.py"):
        # Skip __pycache__ and other build artifacts
        if "__pycache__" not in str(path):
            python_files.append(path)

    return sorted(python_files)


def move_file(old_path: Path, new_path: Path, dry_run: bool = False) -> bool:
    """
    Move a file to a new location, creating directories as needed.

    Args:
        old_path: Current file path
        new_path: Destination file path
        dry_run: If True, only simulate the move

    Returns:
        True if successful (or would be successful in dry run)
    """
    if not old_path.exists():
        print(f"✗ Error: Source file does not exist: {old_path}")
        return False

    if new_path.exists():
        print(f"✗ Error: Destination already exists: {new_path}")
        return False

    if dry_run:
        print(f"  [DRY RUN] Would move: {old_path} -> {new_path}")
        return True

    # Create parent directories if needed
    new_path.parent.mkdir(parents=True, exist_ok=True)

    # Move the file
    shutil.move(str(old_path), str(new_path))

    print(f"✓ Moved: {old_path.name} -> {new_path.relative_to(new_path.parent.parent.parent)}")

    return True


def create_init_files(directory: Path, dry_run: bool = False) -> None:
    """
    Create __init__.py files in directory and all parents up to project root.

    Args:
        directory: Directory to ensure has __init__.py
        dry_run: If True, only simulate creation
    """
    init_file = directory / "__init__.py"

    if not init_file.exists():
        if dry_run:
            print(f"  [DRY RUN] Would create: {init_file}")
        else:
            directory.mkdir(parents=True, exist_ok=True)
            init_file.touch()
            print(f"✓ Created: {init_file}")
