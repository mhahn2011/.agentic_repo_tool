"""Hand-written reference mover for tasks map-and-move cannot do. Run with cwd = fixture worktree:
    python handref.py <plan.json>
Uses the ast module to find import statements (so multi-line and grouped imports work), rewrites them, then
patches dotted-name strings in tests (mock.patch targets) for the moved modules. Stdlib only.
"""
import ast
import json
import re
import subprocess
import sys
from pathlib import Path


def mod_of(path: str) -> str:
    p = Path(path).with_suffix("")
    parts = list(p.parts)
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def apply(moves, root=Path(".")):
    root = Path(root)
    mapping = {mod_of(m["from"]): mod_of(m["to"]) for m in moves}
    # 1. move files, create package dirs with __init__.py
    for m in moves:
        dst = root / m["to"]
        chain, d = [], dst.parent
        while d != root and d != d.parent:
            chain.append(d)
            d = d.parent
        for d in reversed(chain):
            d.mkdir(exist_ok=True)
            if not (d / "__init__.py").exists():
                (d / "__init__.py").write_text("", encoding="utf-8")
        subprocess.run(["git", "mv", m["from"], m["to"]], cwd=root, check=True, capture_output=True)
    # 2. rewrite imports in every .py file
    for f in sorted(root.rglob("*.py")):
        if any(part.startswith(".") for part in f.relative_to(root).parts):
            continue
        rewrite_file(f, root, mapping)


def resolve(module, level, importer_mod, is_pkg):
    if level == 0:
        return module or ""
    base = importer_mod.split(".")
    if not is_pkg:
        base = base[:-1]
    base = base[: len(base) - (level - 1)]
    return ".".join(base + ([module] if module else []))


def rewrite_file(f: Path, root: Path, mapping: dict):
    src = f.read_text(encoding="utf-8")
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return
    rel = f.relative_to(root)
    importer = mapping_inverse_name(rel, mapping)
    is_pkg = f.name == "__init__.py"
    lines = src.splitlines(keepends=True)
    edits = []  # (start_idx, end_idx, new_text)
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            absmod = resolve(node.module, node.level, importer, is_pkg)
            out, changed = [], False
            direct = mapping.get(absmod)
            for al in node.names:
                full = f"{absmod}.{al.name}"
                asname = f" as {al.asname}" if al.asname else ""
                if direct:
                    out.append((direct, al.name + asname)); changed = True
                elif full in mapping:  # from pkg import movedmodule
                    new = mapping[full]
                    parent, leaf = new.rsplit(".", 1)
                    out.append((parent, leaf + asname)); changed = True
                else:
                    out.append((absmod, al.name + asname))
            if changed:
                groups = {}
                for m, n in out:
                    groups.setdefault(m, []).append(n)
                indent = re.match(r"\s*", lines[node.lineno - 1]).group(0)
                stmts = []
                for m, names in groups.items():
                    if node.level and m == absmod:
                        m_txt = "." * node.level + (node.module or "")  # untouched relative form
                    elif node.level:
                        m_txt = relative(m, importer, is_pkg, node.level)
                    else:
                        m_txt = m
                    stmts.append(f"{indent}from {m_txt} import {', '.join(names)}\n")
                edits.append((node.lineno - 1, node.end_lineno, "".join(stmts)))
        elif isinstance(node, ast.Import):
            new_names, changed = [], False
            for al in node.names:
                if al.name in mapping:
                    new_names.append(mapping[al.name] + (f" as {al.asname}" if al.asname else "")); changed = True
                else:
                    new_names.append(al.name + (f" as {al.asname}" if al.asname else ""))
            if changed:
                indent = re.match(r"\s*", lines[node.lineno - 1]).group(0)
                edits.append((node.lineno - 1, node.end_lineno, f"{indent}import {', '.join(new_names)}\n"))
    for s, e, txt in sorted(edits, reverse=True):
        lines[s:e] = [txt]
    text = "".join(lines)
    # 3. dotted-name strings such as mocker.patch("arrow.parser.X")
    # if the file rebinds the top-level package name (e.g. 'from arrow import arrow'), a bare 'arrow.x' is an
    # attribute of that module, not of the package: only rewrite quoted strings there
    try:
        bound = {(al.asname or al.name) for n in ast.walk(ast.parse(text)) if isinstance(n, ast.ImportFrom)
                 for al in n.names}
    except SyntaxError:
        bound = set()
    for old, new in mapping.items():
        if old.split(".")[0] in bound:
            text = re.sub(rf"(?<=[\"'])({re.escape(old)})(?=[.\"'])", new, text)
        else:
            text = re.sub(rf"(?<![\w.])({re.escape(old)})(?![\w])", new, text)  # strings and attribute access
    if text != src:
        f.write_text(text, encoding="utf-8")


def relative(target, importer, is_pkg, level):
    """Best-effort: keep relative style if target shares the importer's package, else absolute."""
    base = importer.split(".")
    if not is_pkg:
        base = base[:-1]
    base = base[: len(base) - (level - 1)]
    t = target.split(".")
    if t[: len(base)] == base:
        return "." * level + ".".join(t[len(base):])
    return target


def mapping_inverse_name(rel: Path, mapping: dict) -> str:
    # importer's module name AFTER the move (its file may itself have been moved already)
    return mod_of(str(rel).replace("\\", "/"))


if __name__ == "__main__":
    plan = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    apply(plan["moves"])
