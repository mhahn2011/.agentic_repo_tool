"""Import parsing - discovering and analyzing Python imports."""

import ast
import re
from pathlib import Path
from typing import Dict, List, Tuple

from models import ImportInfo
from file_operations import find_python_files
from import_resolution import file_path_to_module, resolve_relative_import


def parse_imports(file_path: Path, package_prefix: str = "") -> List[ImportInfo]:
    """
    Parse a Python file and extract all import statements.

    Args:
        file_path: Path to Python file
        package_prefix: Package prefix for detection

    Returns:
        List of ImportInfo objects
    """
    imports = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
            source_lines = source.splitlines()

        tree = ast.parse(source, filename=str(file_path))

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                # Handle: import X, import X as Y
                for alias in node.names:
                    info = ImportInfo(
                        module=alias.name,
                        names=[],
                        alias=alias.asname,
                        is_relative=False,
                        level=0,
                        lineno=node.lineno,
                        raw_line=source_lines[node.lineno - 1].strip(),
                        end_lineno=getattr(node, 'end_lineno', None)
                    )
                    if package_prefix and info.module.startswith(package_prefix + "."):
                        info.is_package_prefixed = True
                        info.original_module_path = info.module
                    imports.append(info)

            elif isinstance(node, ast.ImportFrom):
                # Handle: from X import Y, from .X import Y
                module = node.module or ''
                names = [alias.name for alias in node.names]

                # Check for aliases in 'from X import Y as Z'
                for alias in node.names:
                    info = ImportInfo(
                        module=module,
                        names=[alias.name],
                        alias=alias.asname,
                        is_relative=node.level > 0,
                        level=node.level,
                        lineno=node.lineno,
                        raw_line=source_lines[node.lineno - 1].strip(),
                        end_lineno=getattr(node, 'end_lineno', None)
                    )
                    if package_prefix and info.module.startswith(package_prefix + "."):
                        info.is_package_prefixed = True
                        info.original_module_path = info.module
                    imports.append(info)

    except SyntaxError as e:
        print(f"Warning: Could not parse {file_path}: {e}")
        return []

    return imports


def find_text_based_imports(file_path: Path) -> List[Tuple[int, str]]:
    """
    Find all lines that look like imports using simple text search.

    This intentionally over-matches to catch edge cases that AST might miss.

    Returns:
        List of (line_number, line_content) tuples
    """
    import_lines = []

    # Patterns to match various import forms
    patterns = [
        r'^\s*import\s+[\w.]+',                    # import X or import X.Y.Z
        r'^\s*from\s+[\w.]+\s+import\s+',          # from X import Y
        r'import_module\s*\(',                      # importlib.import_module(
        r'__import__\s*\(',                         # __import__(
        r'exec\s*\(.*import',                       # exec("import X")
        r'eval\s*\(.*import',                       # eval("import X")
    ]

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Warning: Could not read {file_path} for text-based import search: {e}")
        return []

    in_multiline_string = False
    multiline_delimiter = None

    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Track multiline strings
        if '"""' in line or "'''" in line:
            if not in_multiline_string:
                in_multiline_string = True
                multiline_delimiter = '"""' if '"""' in line else "'''"
            elif multiline_delimiter in line:
                in_multiline_string = False
                multiline_delimiter = None

        # Skip if in multiline string or comment
        if in_multiline_string or stripped.startswith('#'):
            continue

        # Check for import patterns
        for pattern in patterns:
            if re.search(pattern, stripped):
                import_lines.append((lineno, stripped))
                break  # Only count each line once

    return import_lines


def classify_uncaught_import(line: str) -> str:
    """
    Classify why an import wasn't caught by AST.

    Returns:
        Human-readable reason string
    """
    line_lower = line.lower()

    if 'import_module' in line:
        return "Dynamic import (importlib.import_module) - not statically analyzable"
    elif '__import__' in line:
        return "Dynamic import (__import__) - not statically analyzable"
    elif 'import *' in line or 'import  *' in line:
        return "Star import (from X import *) - names not resolvable"
    elif 'exec(' in line and 'import' in line:
        return "Import in exec() - not statically analyzable"
    elif 'eval(' in line and 'import' in line:
        return "Import in eval() - not statically analyzable"
    elif line.strip().startswith('#'):
        return "Commented out import (false positive)"
    elif '"""' in line or "'''" in line:
        return "Import in string/docstring (false positive)"
    # Check for package-prefixed absolute imports (e.g., from mypackage.module import X)
    elif re.search(r'from\s+\w+\.\w+', line):
        return "Absolute import with package prefix (e.g., from package.module import X)"
    else:
        return "Unknown - AST parsing may have failed or edge case"


def validate_import_discovery(root_dir: Path,
                               dependency_map: Dict[Path, List[ImportInfo]],
                               moves: List[Tuple[Path, Path]] = None, package_prefix: str = "") -> Dict[Path, List[Tuple[int, str, str]]]:
    """
    Cross-reference AST-parsed imports with text-based search.
    Also check for package-prefixed imports that reference files being moved.

    Args:
        root_dir: Project root directory
        dependency_map: Map of files to AST-parsed imports
        moves: List of (old_path, new_path) tuples being refactored
        package_prefix: Package prefix for resolution

    Returns:
        Dictionary mapping files to list of (lineno, line, reason) for problematic imports
    """
    problematic = {}

    python_files = find_python_files(root_dir)

    # Build map of module paths being moved
    moved_modules = {}
    if moves:
        for old_path, new_path in moves:
            old_module = file_path_to_module(old_path, root_dir, package_prefix)
            moved_modules[old_module] = new_path

    for file_path in python_files:
        # Skip tool files
        if '.tools' in str(file_path):
            continue

        # Get imports from both methods
        text_imports = find_text_based_imports(file_path)
        ast_imports = dependency_map.get(file_path, [])

        # Build set of line numbers that AST found
        ast_lines = {imp.lineno for imp in ast_imports}

        # Find lines that text search found but AST didn't (uncaught imports)
        problematic_lines = []
        for lineno, line in text_imports:
            if lineno not in ast_lines:
                reason = classify_uncaught_import(line)
                # Filter out false positives
                if 'false positive' not in reason.lower():
                    if "Absolute import with package prefix" in reason:
                        continue # No longer a problem
                    problematic_lines.append((lineno, line, reason))

        if problematic_lines:
            problematic[file_path] = problematic_lines

    return problematic


def build_dependency_map(root_dir: Path, package_prefix: str = "") -> Dict[Path, List[ImportInfo]]:
    """
    Build a map of all files and their imports.

    Args:
        root_dir: Root directory of project
        package_prefix: Package prefix for detection

    Returns:
        Dictionary mapping file paths to their imports
    """
    dependency_map = {}

    python_files = find_python_files(root_dir)

    for file_path in python_files:
        imports = parse_imports(file_path, package_prefix)
        dependency_map[file_path] = imports

    return dependency_map


def find_importers(target_file: Path, dependency_map: Dict[Path, List[ImportInfo]],
                   root_dir: Path, package_prefix: str = "") -> List[Tuple[Path, List[ImportInfo]]]:
    """
    Find all files that import from the target file.

    Args:
        target_file: File to search for (e.g., src/math/add.py)
        dependency_map: Map of all file dependencies
        root_dir: Project root directory
        package_prefix: Package prefix for resolution

    Returns:
        List of (importing_file, relevant_imports) tuples
    """
    importers = []

    # Convert target file to module path (e.g., src/math/add.py -> src.math.add)
    target_module = file_path_to_module(target_file, root_dir, package_prefix)

    for file_path, imports in dependency_map.items():
        relevant_imports = []

        for imp in imports:
            if imp.is_relative:
                # Resolve relative import to absolute module path
                resolved = resolve_relative_import(imp, file_path, root_dir, package_prefix)
                if resolved == target_module:
                    relevant_imports.append(imp)
            else:
                # Check if absolute import matches target
                if imp.module == target_module or imp.module.startswith(target_module + '.'):
                    relevant_imports.append(imp)

        if relevant_imports:
            importers.append((file_path, relevant_imports))

    return importers


def discover_imports(project_root: str, package_prefix: str = "") -> Dict[Path, List[ImportInfo]]:
    """
    Main entry point for import discovery.

    Args:
        project_root: Path to project root directory
        package_prefix: Package prefix for detection

    Returns:
        Complete dependency map
    """
    root_path = Path(project_root).resolve()

    print(f"Scanning {root_path} for Python files...")
    dependency_map = build_dependency_map(root_path, package_prefix)

    print(f"Found {len(dependency_map)} Python files")
    total_imports = sum(len(imports) for imports in dependency_map.values())
    print(f"Discovered {total_imports} import statements")

    return dependency_map
