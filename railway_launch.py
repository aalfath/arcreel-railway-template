"""Start ArcReel's server on Railway.

1. Accept Railway's plain postgres:// / postgresql:// DATABASE_URL and switch it to the
   asyncpg driver ArcReel needs.
2. Listen on $PORT (default 1241) on every IPv4 and IPv6 address.
3. ArcReel refuses to start on Linux when bubblewrap can't create namespaces. Railway
   containers don't allow that (no seccomp:unconfined / NET_ADMIN). When the probe fails,
   use ArcReel's own fail-closed fallback (the one it uses on Windows): the agent's Bash
   tool only runs the bundled skill scripts; generation goes through ArcReel's MCP tools.
   When bubblewrap works, nothing changes.
"""
import logging
import os
import platform
import shutil
import subprocess

log = logging.getLogger("railway")

url = os.environ.get("DATABASE_URL", "").strip()
for prefix in ("postgres://", "postgresql://"):
    if url.startswith(prefix):
        os.environ["DATABASE_URL"] = "postgresql+asyncpg://" + url[len(prefix):]
        break


def bwrap_works() -> bool:
    if platform.system() != "Linux" or not shutil.which("bwrap"):
        return False
    try:
        p = subprocess.run(
            ["bwrap", "--unshare-user", "--unshare-net", "--unshare-pid", "--ro-bind", "/", "/", "/bin/true"],
            capture_output=True, timeout=5, check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return p.returncode == 0


import server.app as arcreel_app  # noqa: E402  (after DATABASE_URL is fixed)

if not bwrap_works():
    def _restricted_mode(**_kwargs) -> bool:
        logging.getLogger("server.app").warning(
            "Railway: bubblewrap can't create namespaces in this container, so the agent "
            "Bash sandbox is off and Bash is limited to ArcReel's skill-script allowlist."
        )
        return False

    arcreel_app.check_sandbox_available = _restricted_mode

import uvicorn  # noqa: E402

uvicorn.run(
    arcreel_app.app,
    host="",
    port=int(os.environ.get("PORT") or 1241),
    proxy_headers=True,
    forwarded_allow_ips=os.environ.get("FORWARDED_ALLOW_IPS", "*"),
)
