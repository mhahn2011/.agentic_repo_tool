"""Git integration - version control operations for safe refactoring."""

import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Tuple


def is_git_repo(directory: Path) -> bool:
    """
    Check if directory is a git repository.

    Args:
        directory: Directory to check

    Returns:
        True if directory is a git repository
    """
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--git-dir'],
            cwd=directory,
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False


def get_git_status(directory: Path) -> str:
    """
    Get git status output.

    Args:
        directory: Git repository directory

    Returns:
        Git status output
    """
    try:
        result = subprocess.run(
            ['git', 'status', '--short'],
            cwd=directory,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout
    except Exception as e:
        return f"Error getting git status: {e}"


def has_uncommitted_changes(directory: Path) -> bool:
    """
    Check if repository has uncommitted changes.

    Args:
        directory: Git repository directory

    Returns:
        True if there are uncommitted changes
    """
    status = get_git_status(directory)
    return bool(status.strip())


def git_commit(directory: Path, message: str, allow_empty: bool = False) -> bool:
    """
    Create a git commit.

    Args:
        directory: Git repository directory
        message: Commit message
        allow_empty: Allow empty commits

    Returns:
        True if commit successful
    """
    try:
        # Stage all changes
        subprocess.run(
            ['git', 'add', '-A'],
            cwd=directory,
            check=True,
            capture_output=True,
            timeout=30
        )

        # Commit
        cmd = ['git', 'commit', '-m', message]
        if allow_empty:
            cmd.append('--allow-empty')

        result = subprocess.run(
            cmd,
            cwd=directory,
            capture_output=True,
            text=True,
            timeout=30
        )

        return result.returncode == 0

    except subprocess.CalledProcessError:
        return False
    except Exception as e:
        print(f"Error creating commit: {e}")
        return False


def get_current_commit_hash(directory: Path) -> str:
    """
    Get current commit hash.

    Args:
        directory: Git repository directory

    Returns:
        Commit hash (short form)
    """
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--short', 'HEAD'],
            cwd=directory,
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip()
    except Exception:
        return ""


def git_checkpoint(directory: Path, phase: str, description: str = "") -> Tuple[bool, str]:
    """
    Create a checkpoint commit.

    Args:
        directory: Git repository directory
        phase: Phase name (e.g., 'pre-refactor', 'post-refactor')
        description: Optional description

    Returns:
        Tuple of (success, commit_hash)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if description:
        message = f"[refactor] {phase}: {description}\n\nTimestamp: {timestamp}"
    else:
        message = f"[refactor] {phase}\n\nTimestamp: {timestamp}"

    success = git_commit(directory, message, allow_empty=True)
    commit_hash = get_current_commit_hash(directory) if success else ""

    return (success, commit_hash)


def check_git_safety(directory: Path, skip_git: bool = False) -> Tuple[bool, str]:
    """
    Check if it's safe to proceed with git operations.

    Args:
        directory: Directory to check
        skip_git: Skip git checks

    Returns:
        Tuple of (is_safe, error_message)
    """
    if skip_git:
        return (True, "")

    if not is_git_repo(directory):
        return (False, "Not a git repository. Use --no-commit to skip git integration.")

    if has_uncommitted_changes(directory):
        status = get_git_status(directory)
        return (False, f"Uncommitted changes detected:\n{status}\n\nPlease commit or stash changes before refactoring, or use --no-commit flag.")

    return (True, "")


def git_rollback(directory: Path, commit_hash: str) -> bool:
    """
    Rollback to a specific commit.

    Args:
        directory: Git repository directory
        commit_hash: Commit hash to rollback to

    Returns:
        True if rollback successful
    """
    try:
        result = subprocess.run(
            ['git', 'reset', '--hard', commit_hash],
            cwd=directory,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error during rollback: {e}")
        return False


def generate_refactor_report(moves: List[Tuple[Path, Path]], root_dir: Path,
                            import_updates: dict, config_updates: dict) -> str:
    """
    Generate a summary report of the refactoring.

    Args:
        moves: List of (old_path, new_path) tuples
        root_dir: Project root
        import_updates: Dictionary of import updates
        config_updates: Dictionary of config updates

    Returns:
        Report string
    """
    report = []
    report.append("=" * 60)
    report.append("REFACTORING SUMMARY")
    report.append("=" * 60)
    report.append(f"\nFiles moved: {len(moves)}")

    for old_path, new_path in moves:
        report.append(f"  {old_path.relative_to(root_dir)}")
        report.append(f"    → {new_path.relative_to(root_dir)}")

    if import_updates:
        report.append(f"\nImport statements updated: {sum(len(updates) for updates in import_updates.values())}")
        report.append(f"Files with import updates: {len(import_updates)}")

    if config_updates:
        report.append(f"\nConfiguration files updated: {len(config_updates)}")

    report.append("\n" + "=" * 60)

    return "\n".join(report)
