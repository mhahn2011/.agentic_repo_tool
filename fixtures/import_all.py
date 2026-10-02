"""Import every module under the given top-level packages of a fixture root; report broken imports as JSON.

Usage: python import_all.py <root> <package> [<package> ...]   (run with the fixture's venv python)
Last stdout line is JSON: {"modules": N, "broken": [{"module":..., "error":...}], "skipped_platform": [...]}.
Each module is imported in a subprocess-free loop; a failing import is recorded, not fatal.
"""
import importlib
import json
import re
import sys
import traceback
from pathlib import Path


WINDOWS_ONLY_RE = re.compile(r"only be imported on Windows", re.I)


def module_names(root: Path, package: str):
    pkg_dir = root / package
    if not pkg_dir.is_dir():
        return [package]  # will fail to import and be reported
    names = []
    for f in sorted(pkg_dir.rglob("*.py")):
        rel = f.relative_to(root).with_suffix("")
        parts = list(rel.parts)
        if any(p.startswith(".") or p == "__pycache__" for p in parts):
            continue
        if parts[-1] == "__init__":
            parts = parts[:-1]
        if parts and parts[-1] == "__main__":
            continue
        names.append(".".join(parts))
    return names


def main(argv):
    root = Path(argv[1]).resolve()
    packages = argv[2:] or [p.name for p in root.iterdir() if (p / "__init__.py").exists()]
    sys.path.insert(0, str(root))
    mods, broken, skipped = [], [], []
    for pkg in packages:
        mods += module_names(root, pkg)
    for m in mods:
        try:
            importlib.import_module(m)
        except BaseException as exc:  # noqa: BLE001 - we want every failure recorded
            entry = {"module": m, "error": f"{type(exc).__name__}: {exc}"}
            # a module that refuses to import off Windows (e.g. rich._win32_console) is not a broken import there
            if sys.platform != "win32" and isinstance(exc, ImportError) and WINDOWS_ONLY_RE.search(str(exc)):
                skipped.append(entry)
            else:
                broken.append(entry)
    for b in broken:
        print(f"BROKEN {b['module']}: {b['error']}", file=sys.stderr)
    print(json.dumps({"modules": len(mods), "broken": broken, "skipped_platform": skipped}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
