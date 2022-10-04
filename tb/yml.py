import yaml

import tb.commands as tbc

yml = None


"""
Custom tag handler for managing "!join" tags in yaml files.
"""


def join(loader, node):
    seq = loader.construct_sequence(node)
    return "".join([str(i) for i in seq])


def read_yml():
    with open("./tinderbox.yml", "r") as f:
        try:
            global yml
            loader = yaml.SafeLoader
            loader.add_constructor("!join", join)
            yml = yaml.load(f, loader)
        except yaml.YAMLError as e:
            raise e
    if yml["JOBS"] == 0:
        n = tbc.run("nproc")[1]
        yml["JOBS"] = n
    yml["MAKEOPTS"] = f'-j{yml["JOBS"]} -l{yml["JOBS"]}'
    yml["PORTDIR"] = tbc.run("portageq get_repo_path / gentoo")[1]


def get_yml():
    return yml
