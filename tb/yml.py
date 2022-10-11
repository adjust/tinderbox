import yaml


import tb.commands as tbc


TINDERBOX_CONFIG = "./tinderbox.yml"
"""Path to the tinderbox configuration file."""


class Config:
    """The Config class represents our tinderbox.yml configuration file and
    contains the logic necessary to open and read it."""

    __instance = None
    __yml = None

    def __new__(cls, *args, **kwargs):
        """Override the __new__ method to make sure one and only Config class
        instance exists at all time and is returned by __init__."""
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        """Create an instance of the Config class."""
        if Config.__yml is None:
            Config.__yml = self._read()

    def _join(self, loader, node):
        """Custom tag handler for managing "!join" tags in yaml files.

        Args:
          - loader: a yaml loader.
          - node: the traversed node.

        Returns: a string.
        """
        seq = loader.construct_sequence(node)
        return "".join([str(i) for i in seq])

    def _read(self):
        """Read a path to a YAML file and return the YAML file."

        Returns: a YAML file.
        """
        yml = None
        with open(TINDERBOX_CONFIG, "r") as f:
            try:
                loader = yaml.SafeLoader
                loader.add_constructor("!join", self._join)
                yml = yaml.load(f, loader)
            except yaml.YAMLError as e:
                raise e
        if yml["JOBS"] == 0:
            n = tbc.run("nproc")[1]
            yml["JOBS"] = n
        yml["MAKEOPTS"] = f'-j{yml["JOBS"]} -l{yml["JOBS"]}'
        yml["PORTDIR"] = tbc.run("portageq get_repo_path / gentoo")[1]
        return yml

    def get(self):
        """Return the YAML file.

        Returns: a YAML file.
        """
        return Config.__yml
