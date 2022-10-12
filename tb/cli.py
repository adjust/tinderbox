import logging
import sys

import docopt

import tb.backend as tbb

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s][%(name)s][%(levelname)s]: %(message)s"
)
logger = logging.getLogger(__name__)


__version__ = "1.0"
__author__ = "adjust OS team"
__email__ = "platform.os@adjust.com"
__date__ = "30/09/2022"
__credits__ = "adjust OS team"


class Tinderbox:
    """tinderbox: a Python script to drive the binary package compilation process.

Usage:
  tinderbox [-h|--help] [-v|--version] <command>

Commands:
  tinderbox clean_targets   clean targets directory.
  tinderbox create_targets  create targets directory.
  tinderbox prepare         compile base packages for all targets.
  tinderbox compile         compile system and world packages for all targets.
  tinderbox all             all of the above.

Options:
    -h,  --help        display help.
    -v,  --version     display version."""

    def __init__(self):
        args = docopt.docopt(
            Tinderbox.__doc__, version=__version__, help=True, options_first=True
        )

        runner = {
            "clean_targets": tbb.clean_targets,
            "create_targets": tbb.create_targets,
            "prepare": tbb.prepare,
            "compile": tbb.compile_packages,
            "all": tbb.run,
        }

        try:
            runner[args["<command>"]]()
        except KeyError:
            sys.exit(
                """Error! \'%s\' is an invalid command!
See 'tinderbox --help' for a complete list of commands."""
                % (args["<command>"])
            )


if __name__ == "__main__":
    sys.exit(Tinderbox())
