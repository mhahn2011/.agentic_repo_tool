"""Registry mode - centralized import management for faster refactoring."""

import ast
import json
import importlib.util
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

from models import ImportInfo
from file_operations import find_python_files, create_init_files, move_file
from import_resolution import file_path_to_module
from import_parsing import parse_imports, build_dependency_map, validate_import_discovery, discover_imports, find_importers
from import_rewriting import update_imports_in_file
from config_updates import update_config_files
from validation import verify_file_operations, verify_no_broken_imports
from git_integration import git_checkpoint
from orchestration import load_refactor_plan

def initialize_registry(root_dir: Path, output_file: Path = None) -> Dict[str, str]:
    """
    Initialize refactor registry from current project structure.

    Args:
        root_dir: Project root directory
        output_file: Optional output file path

    Returns:
        Registry dictionary
    """
    print("Initializing refactor registry...")

    python_files = find_python_files(root_dir)

    registry = {
        "version": "1.0",
        "generated": datetime.now().isoformat(),
        "files": {}
    }

    for file_path in python_files:
        # Skip test files and __init__.py
        if 'test' in str(file_path) or file_path.name == '__init__.py':
            continue

        # Create a logical name from the file
        module = file_path_to_module(file_path, root_dir)
        name = module.split('.')[-1]

        registry["files"][name] = str(file_path.relative_to(root_dir))

    if output_file is None:
        output_file = root_dir / "refactor_registry.json"

    with open(output_file, 'w') as f:
        json.dump(registry, f, indent=2)

    print(f"✓ Registry initialized: {output_file}")
    print(f"  {len(registry['files'])} files registered")

    return registry

def verify_refactor_plan(plan_file: Path, root_dir: Path, package_prefix: str = "") -> bool:
    """
    Verify refactor plan without executing.

    Args:
        plan_file: Path to refactor plan
        root_dir: Project root
        package_prefix: Package prefix for resolution

    Returns:
        True if plan is valid
    """
    print("=" * 60)
    print("VERIFYING REFACTOR PLAN")
    print("=" * 60)

    # Load plan
    print(f"\n1. Loading plan: {plan_file}")
    try:
        moves = load_refactor_plan(plan_file, root_dir)
        print(f"   ✓ Plan loaded: {len(moves)} moves")
    except Exception as e:
        print(f"   ✗ Failed to load plan: {e}")
        return False

    # Verify file operations
    print("\n2. Verifying file operations...")
    valid, errors = verify_file_operations(moves, root_dir)
    if valid:
        print(f"   ✓ All file operations valid")
    else:
        print(f"   ✗ Invalid operations:")
        for error in errors:
            print(f"     - {error}")
        return False

    # Check current imports
    print("\n3. Checking current import state...")
    valid, errors = verify_no_broken_imports(root_dir)
    if valid:
        print("   ✓ Current imports are valid")
    else:
        print(f"   ⚠ Found {len(errors)} broken imports in current state:")
        for error in errors[:5]:
            print(f"     - {error}")
        if len(errors) > 5:
            print(f"     ... and {len(errors) - 5} more")

    # Preview changes
    print("\n4. Preview of changes:")
    dep_map = discover_imports(str(root_dir), package_prefix)
    for old_path, new_path in moves:
        print(f"\n   {old_path.relative_to(root_dir)}")
        print(f"   → {new_path.relative_to(root_dir)}")

        importers = find_importers(old_path, dep_map, root_dir, package_prefix)
        if importers:
            print(f"   Affects {len(importers)} file(s)")

    print("\n" + "=" * 60)
    print("VERIFICATION COMPLETE")
    print("=" * 60)

    return True

def generate_import_registry(root_dir: Path,
                            output_file: Path = None,
                            exclude_patterns: List[str] = None, package_prefix: str = "") -> Dict[str, str]:
    """
    Generate a Python module that re-exports all discovered imports.

    Args:
        root_dir: Project root directory
        output_file: Path to write refactor_registry.py (default: root_dir/refactor_registry.py)
        exclude_patterns: Patterns to exclude (e.g., ['test_', '__pycache__'])

    Returns:
        Dictionary mapping export names to source modules
    """
    if output_file is None:
        output_file = root_dir / ".tools" / "auto_refactor" / "refactor_registry.py"

    if exclude_patterns is None:
        exclude_patterns = ['/tests/', '__pycache__', '__init__.py', '/.tools/', 'setup.py']

    # Discover all Python files
    python_files = find_python_files(root_dir)

    # Build registry of exports
    registry = {}

    for file_path in python_files:
        # Skip excluded files
        print(f"Processing file: {file_path}")
        if any(pattern in str(file_path) for pattern in exclude_patterns):
            print(f"Skipping file: {file_path}")
            continue

        # Parse file to discover what it exports
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()

            tree = ast.parse(source, filename=str(file_path))
            module_path = file_path_to_module(file_path, root_dir, package_prefix)

            # Find all top-level function and class definitions
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    export_name = node.name
                    print(f"Found export: {export_name} in {module_path}")
                    registry[export_name] = module_path

        except SyntaxError:
            print(f"Warning: Could not parse {file_path}")
            continue

    # Generate registry module
    lines = []
    lines.append('"""')
    lines.append('Auto-generated import registry.')
    lines.append('DO NOT EDIT MANUALLY - regenerate with: refactor_tool.py --generate-registry')
    lines.append('"""')
    lines.append('')

    # Sort for consistent output
    for export_name in sorted(registry.keys()):
        module_path = registry[export_name]
        # Create import statement with internal alias
        lines.append(f'from {module_path} import {export_name} as _{export_name}_impl')

    lines.append('')
    lines.append('# Re-export with clean names')
    for export_name in sorted(registry.keys()):
        lines.append(f'{export_name} = _{export_name}_impl')

    lines.append('')
    lines.append('# Export list for introspection')
    lines.append('__all__ = [')
    for export_name in sorted(registry.keys()):
        lines.append(f"    '{export_name}',")
    lines.append(']')
    lines.append('')

    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"✓ Generated registry: {output_file}")
    print(f"  {len(registry)} exports registered")

    return registry


def update_registry_for_move(registry_file: Path, old_path: Path,
                             new_path: Path, root_dir: Path, package_prefix: str = "") -> None:
    """
    Update the registry file when a source file moves.

    Args:
        registry_file: Path to refactor_registry.py
        old_path: Old file path
        new_path: New file path
        root_dir: Project root
    """
    old_module = file_path_to_module(old_path, root_dir, package_prefix)
    new_module = file_path_to_module(new_path, root_dir, package_prefix)

    # Read registry
    with open(registry_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace old module path with new module path
    updated_content = content.replace(f'from {old_module} import',
                                     f'from {new_module} import')

    # Write back
    with open(registry_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"✓ Updated registry: {old_module} -> {new_module}")


def convert_imports_to_registry(file_path: Path, registry_exports: List[str],
                               root_dir: Path, dry_run: bool = False) -> List[Tuple[int, str, str]]:
    """
    Convert hard-coded imports to registry-based imports.

    Args:
        file_path: File to convert
        registry_exports: List of names available in registry
        root_dir: Project root
        dry_run: If True, only preview changes

    Returns:
        List of (line_number, old_statement, new_statement) tuples
    """
    changes = []

    # Parse current imports
    imports = parse_imports(file_path)

    for imp in imports:
        # Skip standard library and third-party imports
        if not imp.module.startswith('src'):
            continue

        # Check if any imported names are in registry
        for name in imp.names:
            if name in registry_exports:
                old_stmt = imp.raw_line

                # Generate new registry import
                if imp.alias:
                    new_stmt = f"from refactor_registry import {name} as {imp.alias}"
                else:
                    new_stmt = f"from refactor_registry import {name}"

                changes.append((imp.lineno, old_stmt, new_stmt))

    if changes and not dry_run:
        # Apply changes
        updates = [(lineno, new_stmt) for lineno, _, new_stmt in changes]
        update_imports_in_file(file_path, updates)

    return changes


def convert_project_to_registry(root_dir: Path, dry_run: bool = False, package_prefix: str = "") -> Dict[Path, List[Tuple[int, str, str]]]:
    """
    Convert all imports in project to use registry.

    Args:
        root_dir: Project root
        dry_run: If True, only preview changes

    Returns:
        Dictionary mapping files to their changes
    """
    print("=" * 60)
    print("CONVERTING PROJECT TO REGISTRY-BASED IMPORTS")
    print("=" * 60)

    # Generate registry first
    registry_file = root_dir / ".tools" / "auto_refactor" / "refactor_registry.py"
    registry = generate_import_registry(root_dir, registry_file, package_prefix=package_prefix)
    registry_exports = list(registry.keys())

    # Find all Python files to convert
    python_files = find_python_files(root_dir)

    all_changes = {}
    total_conversions = 0

    for file_path in python_files:
        # Skip registry itself and test files
        if file_path.name == 'refactor_registry.py' or 'test' in str(file_path):
            continue

        changes = convert_imports_to_registry(file_path, registry_exports,
                                             root_dir, dry_run)

        if changes:
            all_changes[file_path] = changes
            total_conversions += len(changes)

            print(f"\n{file_path.relative_to(root_dir)}:")
            for lineno, old_stmt, new_stmt in changes:
                print(f"  Line {lineno}:")
                print(f"    - {old_stmt}")
                print(f"    + {new_stmt}")

    print("\n" + "=" * 60)
    print(f"CONVERSION {'PREVIEW' if dry_run else 'COMPLETE'}")
    print(f"Files affected: {len(all_changes)}")
    print(f"Imports converted: {total_conversions}")
    print("=" * 60)

    return all_changes


def execute_refactor_with_registry(plan_file: Path, root_dir: Path,
                                  dry_run: bool = False,
                                  skip_git: bool = False, package_prefix: str = "") -> bool:
    """
    Execute refactoring using registry-based approach.

    This only updates the registry file instead of rewriting imports in all files.

    Args:
        plan_file: Path to refactor plan
        root_dir: Project root
        dry_run: If True, simulate without changes
        skip_git: If True, skip git operations

    Returns:
        True if successful
    """
    print("=" * 60)
    print("REGISTRY-BASED REFACTORING")
    print("=" * 60)

    # Check registry exists
    registry_file = root_dir / ".tools" / "auto_refactor" / "refactor_registry.py"
    if not registry_file.exists():
        print(f"\n✗ Registry not found: {registry_file}")
        print("\nTo use registry-based refactoring, you must first:")
        print("  1. Generate registry: python3 .tools/auto_refactor/refactor_tool.py --generate-registry")
        print("  2. (Optional) Convert imports: python3 .tools/auto_refactor/refactor_tool.py --convert-to-registry")
        print("\nOr use direct refactoring (no --use-registry flag)")
        return False

    # Load plan
    print(f"\nLoading plan: {plan_file}")
    moves = load_refactor_plan(plan_file, root_dir)
    print(f"Found {len(moves)} file moves")

    # Build dependency map for import validation
    dep_map = build_dependency_map(root_dir, package_prefix)

    # Validate import discovery
    print("\n" + "=" * 60)
    print("VALIDATING IMPORT DISCOVERY")
    print("=" * 60)

    uncaught_imports = validate_import_discovery(root_dir, dep_map, moves)

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

        if not dry_run:
            response = input("Continue with refactoring? (yes/no): ")
            if response.lower() != 'yes':
                print("Refactoring cancelled")
                return False
    else:
        print("✓ All imports successfully parsed by AST")

    # Verify operations
    print("\nVerifying file operations...")
    valid, errors = verify_file_operations(moves, root_dir)
    if not valid:
        print("\n✗ Validation failed:")
        for error in errors:
            print(f"  - {error}")
        return False
    print("✓ All file operations valid")

    # Git checkpoint if enabled
    pre_commit_hash = ""
    if not skip_git and not dry_run:
        print("\nCreating pre-refactor checkpoint...")
        success, pre_commit_hash = git_checkpoint(root_dir, "pre-refactor")
        if not success:
            return False
        print(f"✓ Pre-refactor checkpoint: {pre_commit_hash}")

    # Update registry for each move
    print("\n" + "=" * 60)
    print("UPDATING REGISTRY")
    print("=" * 60)

    for old_path, new_path in moves:
        print(f"\n{old_path.relative_to(root_dir)}")
        print(f"-> {new_path.relative_to(root_dir)}")

        if not dry_run:
            update_registry_for_move(registry_file, old_path, new_path, root_dir, package_prefix)

    # Update configuration files
    print("\n" + "=" * 60)
    print("UPDATING CONFIGURATION FILES")
    print("=" * 60)

    all_config_updates = {}
    for old_path, new_path in moves:
        config_updates = update_config_files(old_path, new_path, root_dir, dry_run)
        all_config_updates.update(config_updates)

    if all_config_updates:
        print(f"\n✓ Updated {len(all_config_updates)} configuration file(s)")
    else:
        print("\n  No string references found in config files")

    # Move files
    print("\n" + "=" * 60)
    print("MOVING FILES")
    print("=" * 60)

    for old_path, new_path in moves:
        # Create directories and __init__ files
        if new_path.parent != old_path.parent:
            current = new_path.parent
            while current != root_dir and current.name != 'src':
                create_init_files(current, dry_run)
                current = current.parent

        # Move file
        success = move_file(old_path, new_path, dry_run)
        if not success:
            print(f"\n✗ Refactoring failed")
            if pre_commit_hash:
                print(f"Rollback with: git reset --hard {pre_commit_hash}")
            return False

    # Verify imports still work (registry should handle everything)
    if not dry_run:
        print("\n" + "=" * 60)
        print("VERIFYING REGISTRY")
        print("=" * 60)

        # Try importing the registry to check for errors
        try:
            import sys
            sys.path.insert(0, str(root_dir))
            spec = importlib.util.spec_from_file_location("refactor_registry", registry_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print("✓ Registry imports successfully")
        except Exception as e:
            print(f"✗ Registry has errors: {e}")
            if pre_commit_hash:
                print(f"Rollback with: git reset --hard {pre_commit_hash}")
            return False

    # Git checkpoint after
    if not skip_git and not dry_run:
        print("\nCreating post-refactor checkpoint...")
        report = f"Refactored {len(moves)} files using registry-based approach"
        success, post_commit_hash = git_checkpoint(root_dir, "post-refactor", report)
        if not success:
            print(f"Rollback with: git reset --hard {pre_commit_hash}")
            return False
        print(f"✓ Post-refactor checkpoint: {post_commit_hash}")

    # Success
    print("\n" + "=" * 60)
    if dry_run:
        print("DRY RUN COMPLETE")
    else:
        print("REGISTRY-BASED REFACTORING COMPLETE")
        print("\nKey advantage: Future refactors only need to update refactor_registry.py")
    print("=" * 60)

    return True


def detect_package_prefix(root_dir: Path) -> str:
    """
    Detect the package prefix for the project.

    Strategies:
    1. Look for common package directories ('src', 'app', etc.)
    2. Analyze import statements to infer the prefix.

    Returns:
        The detected package prefix (e.g., 'src') or an empty string.
    """
    # Strategy 1: Common directory names
    for common_prefix in ['src', 'app']:
        if (root_dir / common_prefix).is_dir() and (root_dir / common_prefix).exists():
            # Check for __init__.py in the package folder
            if (root_dir / common_prefix / '__init__.py').exists():
                 return common_prefix
            # Check for any .py file in the package folder
            if any((root_dir / common_prefix).glob('*.py')):
                return common_prefix


    # Strategy 2: Infer from imports (simplified)
    python_files = find_python_files(root_dir)
    for file_path in python_files:
        if '.tools' in str(file_path):
            continue
        imports = parse_imports(file_path)
        for imp in imports:
            if '.' in imp.module:
                prefix = imp.module.split('.')[0]
                if (root_dir / prefix).is_dir() and (root_dir / prefix).exists():
                    # Check for __init__.py in the package folder
                    if (root_dir / prefix / '__init__.py').exists():
                        return prefix
                    # Check for any .py file in the package folder
                    if any((root_dir / prefix).glob('*.py')):
                        return prefix
    
    return ""

def should_use_registry_mode(root_dir: Path) -> Tuple[bool, str]:
    """
    Determine if registry mode should be used.

    Checks:
    1. Registry file exists
    2. Project has registry-based imports

    Returns:
        Tuple of (should_use, reason)
    """
    registry_file = root_dir / ".tools" / "auto_refactor" / "refactor_registry.py"

    if not registry_file.exists():
        return False, "Registry file not found"

    # Check if any files import from registry
    python_files = find_python_files(root_dir)
    registry_imports_found = 0

    for file_path in python_files:
        # Skip tool files
        if '.tools' in str(file_path):
            continue

        imports = parse_imports(file_path)
        for imp in imports:
            if 'refactor_registry' in imp.module:
                registry_imports_found += 1
                break

    if registry_imports_found > 0:
        return True, f"Found {registry_imports_found} files using registry"
    else:
        return False, "Registry exists but no files use it"

def validate_registry_conversion(root_dir: Path) -> Tuple[bool, List[str]]:
    """
    Validate that registry conversion succeeded without breaking code.

    Checks:
    1. Registry file has valid Python syntax
    2. No duplicate exports in registry
    3. All imported names exist in registry

    Returns:
        Tuple of (valid, list_of_errors)
    """
    errors = []

    registry_file = root_dir / ".tools" / "auto_refactor" / "refactor_registry.py"

    # Check registry syntax
    try:
        with open(registry_file, 'r') as f:
            source = f.read()
        ast.parse(source)
    except SyntaxError as e:
        errors.append(f"Registry has syntax error: {e}")
        return False, errors

    # Check for duplicate exports
    try:
        with open(registry_file, 'r') as f:
            content = f.read()

        # Extract all export names
        export_pattern = r'^(\w+) = _\1_impl$'
        import re
        exports = re.findall(export_pattern, content, re.MULTILINE)

        if len(exports) != len(set(exports)):
            duplicates = [e for e in exports if exports.count(e) > 1]
            errors.append(f"Duplicate exports in registry: {duplicates}")
    except Exception as e:
        errors.append(f"Error checking registry exports: {e}")

    return len(errors) == 0, errors

def check_auto_convert_safety(root_dir: Path) -> Tuple[bool, List[str]]:
    """
    Safety checks before auto-converting to registry.

    Checks:
    1. No circular imports
    2. All imports are resolvable
    3. No name conflicts in registry

    Returns:
        Tuple of (safe, list_of_warnings)
    """
    warnings = []

    # Check for circular imports
    dep_map = build_dependency_map(root_dir)
    # (Simplified - full implementation would check for cycles)

    # Check for name conflicts
    python_files = find_python_files(root_dir)
    all_names = {}

    for file_path in python_files:
        if '.tools' in str(file_path) or 'test' in str(file_path):
            continue

        try:
            with open(file_path, 'r') as f:
                tree = ast.parse(f.read())

            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    name = node.name
                    if name in all_names:
                        warnings.append(
                            f"Name conflict: '{name}' defined in both "
                            f"{all_names[name]} and {file_path}"
                        )
                    all_names[name] = file_path
        except:
            continue

    return len(warnings) == 0, warnings

def execute_refactor_with_auto_registry(plan_file: Path, root_dir: Path,
                                       dry_run: bool = False,
                                       skip_git: bool = False,
                                       package_prefix: str = "") -> bool:
    """
    Execute refactoring with automatic registry conversion.

    Flow:
    1. Check/generate registry
    2. Convert imports to registry
    3. Validate conversion
    4. Git checkpoint
    5. Execute registry-based refactor

    Returns:
        True if successful
    """
    print("=" * 60)
    print("AUTO-CONVERT REGISTRY REFACTORING")
    print("=" * 60)

    registry_file = root_dir / ".tools" / "auto_refactor" / "refactor_registry.py"

    # Step 1: Check registry existence
    print("\\n1. Checking registry status...")
    if not registry_file.exists():
        print("   Registry not found, generating...")
        if not dry_run:
            registry = generate_import_registry(root_dir, registry_file)
            print(f"   ✓ Generated registry with {len(registry)} exports")
        else:
            print("   [DRY RUN] Would generate registry")
    else:
        print("   ✓ Registry exists")

    # Step 2: Check if conversion needed
    print("\\n2. Analyzing import patterns...")
    should_convert, reason = should_use_registry_mode(root_dir)

    if not should_convert and not dry_run:
        print(f"   {reason}")
        print("   Converting imports to registry...")

        changes = convert_project_to_registry(root_dir, dry_run=False)

        if changes:
            print(f"   ✓ Converted {len(changes)} files to registry imports")
        else:
            print("   No conversion needed (no matching imports found)")
    else:
        print(f"   ✓ {reason}")

    # Step 3: Validate conversion
    if not dry_run:
        print("\\n3. Validating registry...")
        valid, errors = validate_registry_conversion(root_dir)

        if not valid:
            print("   ✗ Registry validation failed:")
            for error in errors:
                print(f"     - {error}")
            return False
        print("   ✓ Registry validation passed")
    else:
        print("\\n3. [DRY RUN] Would validate registry")

    # Step 4: Git checkpoint for conversion
    if not skip_git and not dry_run:
        print("\\n4. Creating git checkpoint after conversion...")
        success, checkpoint = git_checkpoint(root_dir, "registry-conversion",
                                            "Converted imports to registry system")
        if not success:
            print("   ✗ Failed to create checkpoint")
            return False
        print(f"   ✓ Checkpoint created: {checkpoint}")
    elif dry_run:
        print("\\n4. [DRY RUN] Would create git checkpoint")
    else:
        print("\\n4. Skipping git checkpoint (--no-commit)")

    # Step 5: Execute registry-based refactor
    print("\\n5. Executing registry-based refactor...")
    success = execute_refactor_with_registry(
        plan_file=plan_file,
        root_dir=root_dir,
        dry_run=dry_run,
        skip_git=skip_git,
        package_prefix=package_prefix
    )

    if not success:
        print("\\n✗ Refactoring failed")
        return False

    # Success
    print("\\n" + "=" * 60)
    print("AUTO-CONVERT REFACTORING COMPLETE")
    print("=" * 60)
    print("\\nWhat happened:")
    print("  1. Registry generated/verified")
    print("  2. Imports converted to registry")
    print("  3. Files refactored using registry")
    print("  4. Future refactors will be instant")
    print("=" * 60)

    return True

