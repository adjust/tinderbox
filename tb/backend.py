import glob
import logging
import os
import shutil

import tb.commands as tbc
import tb.yml as tbyml
from tb.emerge import Emerge
from tb.templates import UPDATE_SINGLE_TARGET, CREATE_TARGETS


tbyml.read_yml()
yml = tbyml.get_yml()


logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s][%(name)s][%(levelname)s]: %(message)s"
)
logger = logging.getLogger(__name__)


my_env = {
    "PORTAGE_COMPRESSION_COMMAND": yml["PORTAGE_COMPRESSION_COMMAND"],
    "ACCEPT_PROPERTIES": yml["ACCEPT_PROPERTIES"],
    "PORTAGE_BINHOST": yml["PORTAGE_BINHOST"],
    "GCC_COLORS": yml["GCC_COLORS"],
    "FEATURES": yml["FEATURES"],
    "MAKEOPTS": yml["MAKEOPTS"],
    "PORTDIR": yml["PORTDIR"],
    "PKGDIR": yml["PKGDIR"],
}


def run():
    clean_targets()
    create_targets()
    prepare()
    compile_packages()
    logger.info("Run complete!")


def clean_targets():
    for target in glob.glob(f'{yml["TARGETSDIR"]}/confs/*'):
        if not os.path.isdir(target):
            continue
        logger.info(f"Deleting directory {target}")
        shutil.rmtree(target)


def set_profile(target):
    try:
        os.remove(f"{target}/etc/portage/make.profile")
    except Exception:
        pass
    logger.info(f"Setting amd64/17.0/no-multilib profile in {target}")
    os.symlink(
        f'{yml["PORTDIR"]}/profiles/default/linux/amd64/17.0/no-multilib',
        f"{target}/etc/portage/make.profile",
    )


def prepare():
    emerge = Emerge(env=my_env)
    for target in iter(os.listdir(yml["TARGETSDIR"])):
        if not os.path.isdir(os.path.join(yml["TARGETSDIR"], target)):
            continue

        update_single_target(target=target, root=yml["TARGETSDIR"])
        os.chdir(yml["TARGETSDIR"])
        set_profile(target)
        emerge.target(target)

        emerge.args("--nodep --oneshot baselayout").run()
        emerge.args("--nodep --oneshot app-portage/elt-patches").run()
        emerge.args("--root-deps=rdeps --oneshot virtual/libc").run()

        my_env["USE"] = "internal-glib"
        emerge.env(my_env).args("--buildpkg=n --oneshot virtual/pkgconfig").run()
        my_env.pop("USE")

        emerge.env(my_env).args("--root-deps=rdeps --oneshot dev-lang/perl").run()

        my_env["USE"] = "-gpg -nls"
        emerge.env(my_env).args("--buildpkg=n --oneshot dev-vcs/git").run()
        my_env.pop("USE")

        emerge.env(my_env).args("--oneshot sys-devel/gettext").run()
        emerge.args("--keep-going @system").run()


def create_targets():
    os.chdir(yml["REPODIR"])
    command = CREATE_TARGETS.format(root=yml["TARGETSDIR"])
    logger.info(f"Running '{command}'")
    tbc.run(command)


def update_single_target(target, root):
    os.chdir(yml["REPODIR"])
    command = UPDATE_SINGLE_TARGET.format(target=target, root=root)
    logger.info(f"Running '{command}'")
    tbc.run(command)


def compile_packages():
    emerge = Emerge(env=my_env)
    for target in iter(os.listdir(yml["TARGETSDIR"])):
        update_single_target(target=target, root=yml["TARGETSDIR"])
        os.chdir(yml["TARGETSDIR"])
        set_profile(target)
        emerge.target(target)
        emerge.args("@system").run()
        world_path = f'{yml["TARGETSDIR"]}/{target}/etc/portage/world'
        with open(world_path, "r") as world_file:
            for line in world_file:
                pkg = line.strip()
                emerge.args(f"{pkg}").run()
                emerge.args(f"--root-deps {pkg}").run()
    emerge.args("@world").run()
