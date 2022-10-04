#!/usr/bin/env python3
"""the adjust tinderbox

Usage:
  tinderbox.py
  tinderbox.py (-h | --help)
  tinderbox.py (-m | --man)
  tinderbox.py --version

Options:
    -h|--help     display help.
    -m|--man      display man page.
    --version     display version.
"""


__version__ = "0.0.1"
__author__ = "OS team <ops@adjust.com>"
__date__ = "30/09/2022"
__credits__ = "adjust OS team"


import logging
import pydoc
import sys

import docopt

import tb.backend as tbb

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s][%(name)s][%(levelname)s]: %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Main function."""
    argv = docopt.docopt(__doc__)
    if argv["-m"] or argv["--man"]:
        pydoc.doc(__file__.replace(".py", "").replace("./", ""))
    logger.info("Running tinderbox with the following options:")
    logger.info(dict(argv))
    tbb.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
