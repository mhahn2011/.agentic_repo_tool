"""C1.18 MissionHub index check exits 0."""
from common import MISSIONHUB, PY, finish, sh

rc, out = sh([PY, "system/execution-context/tcds/build_index.py", "--check"], cwd=MISSIONHUB)
finish(rc == 0, out.strip()[-300:])
