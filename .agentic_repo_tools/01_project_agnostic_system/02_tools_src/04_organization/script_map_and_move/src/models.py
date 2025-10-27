"""Data models for the refactor tool."""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ImportInfo:
    """Information about a single import statement."""
    module: str  # Module being imported (e.g., 'src.math.add')
    names: List[str]  # Names imported (e.g., ['add']) or empty for 'import X'
    alias: Optional[str]  # Alias if used (e.g., 'fmt' in 'import X as fmt')
    is_relative: bool  # True if relative import (starts with .)
    level: int  # Number of dots in relative import (0 for absolute)
    lineno: int  # Line number in source file (start line for multiline imports)
    raw_line: str  # Original import line as string
    end_lineno: Optional[int] = None  # End line number for multiline imports
    is_package_prefixed: bool = False
    original_module_path: str = ""
