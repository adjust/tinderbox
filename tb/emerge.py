import logging

import tb.commands as tbc
import tb.yml as tyml
from tb.templates import EMERGE


yml = tyml.Config().get()


logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s][%(name)s][%(levelname)s]: %(message)s"
)
logger = logging.getLogger(__name__)


class Emerge:
    def __init__(self, env="", target=""):
        self._env = env
        self._target = target
        self._args = ""

    def env(self, env):
        self._env = env
        return self

    def target(self, target):
        self._target = target
        return self

    def args(self, args):
        self._args = args
        return self

    def run(self):
        e = self.eformat()
        logger.info(f"Running the following 'emerge' command:\n{e}")
        tbc.run(self.eformat(), env=self._env)

    def eformat(self):
        target = self._target
        emerge = EMERGE.format(
            bin_exclude=yml["BINEXCLUDE"],
            exclude=yml["EXCLUDE"],
            config_root=f'{yml["TARGETSDIR"]}/{target}',
            jobs=yml["JOBS"],
            root=f'{yml["ROOTSDIR"]}/{target}',
        )
        if self._args != "":
            emerge += " " + self._args
        return emerge
