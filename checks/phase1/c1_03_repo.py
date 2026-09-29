"""C1.3 Harness repo cloned and remote owner equals the gh login."""
from common import ROOT, finish, sh

rc, login = sh(["gh", "api", "user", "-q", ".login"])
login = login.strip()
rc2, remotes = sh(["git", "-C", str(ROOT), "remote", "-v"])
want = f"github.com/{login}/.agentic_repo_tool"
finish(rc == 0 and rc2 == 0 and want in remotes, f"login={login!r} want {want} in:\n{remotes}")
