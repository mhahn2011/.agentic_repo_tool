"""C1.12 Grader validated: reference passes, untouched fixture fails, for every task in the suite."""
from common import PY, ROOT, finish, sh

rc, out = sh([PY, str(ROOT / "runner" / "validate_grader.py"), "mm-arrow"], timeout=1800)
finish(rc == 0, out.strip()[-1500:])
