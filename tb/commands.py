import logging
import os
import shlex
import subprocess

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s][%(name)s][%(levelname)s]: %(message)s"
)
logger = logging.getLogger(__name__)


def run(cmd, env=None):
    if not cmd:
        return
    cmd = shlex.split(cmd)
    if env is not None:
        e = os.environ.copy()
        env = {**e, **env}
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=env)
    stdout, stderr = process.communicate()
    stdout = stdout.decode("utf-8").strip()
    rc = process.returncode
    return (rc, stdout, stderr)
