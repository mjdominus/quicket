
import fcntl
from os import environ as env
from pathlib import Path
import pwd
import toml


class Quicket():
    def __init__(self, config_dir=None):
        if config_dir is None:
            config_dir = self.default_config_dir()
        self.config_dir = Path(config_dir)

        self.configure()

    def default_config_dir(self):
        if "QUICKET_HOME" in env:
            return Path(env["QUICKET_HOME"])
        else:
            return self.homedir / ".quicket"

    def default_config_file(self):
        if "QUICKET_CONF" in env:
            return Path(env["QUICKET_CONF"])
        else:
            return self.default_config_dir() / "config"

    @property
    def homedir(self):
        if "HOME" in env:
            return Path(env["HOME"])
        else:
            uid = os.getuid()
            return Path(pwd.getpwuid(uid).pw_dir)

    def configure(self):
        try:
            with open(self.default_config_file()) as fh:
                self.conf = toml.load(fh)
        except FileNotFoundError:
            self.conf = {}

    @property
    def ticket_dir(self):
        return "/home/mjd/quicket" # XXX

    @property
    def template_file(self):
        return self.config_dir / "template.md"
