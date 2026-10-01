"""C1.4: Harbor installed. `harbor --version` prints a version, exit 0 (native Windows install via uv tool)."""
import os
from pathlib import Path
from common import finish, sh

HARBOR = str(Path.home() / ".local" / "bin" / "harbor.exe")
rc, out = sh([HARBOR, "--version"], timeout=60)
finish(rc == 0 and out.strip() != "", f"rc={rc} harbor {out.strip()}")
