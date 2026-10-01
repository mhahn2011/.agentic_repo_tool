"""C1.2: Docker works from WSL. `wsl -e docker run --rm hello-world` prints 'Hello from Docker!', exit 0."""
from common import finish, sh

rc, out = sh(["wsl", "-e", "docker", "run", "--rm", "hello-world"], timeout=180)
finish(rc == 0 and "Hello from Docker!" in out, f"rc={rc} " + out.strip().splitlines()[-1] if out.strip() else f"rc={rc} no output")
