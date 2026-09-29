"""C1.1 WSL2 present: default version 2, one Ubuntu distro."""
from common import finish, sh

rc1, st = sh(["wsl", "--status"])
rc2, lst = sh(["wsl", "-l", "-v"])
ok = rc1 == 0 and rc2 == 0 and "Default Version: 2" in st and "Ubuntu" in lst
finish(ok, f"status rc={rc1}, list rc={rc2}\n{st.strip()}\n{lst.strip()}")
