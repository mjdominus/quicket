
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

        if "id-format" not in self.conf:
            self.conf["id-format"] = "{:03d}"

        if "ticket-dir" not in self.conf:
            self.conf["ticket-dir"] = self.homedir / "quicket"

    def allocate_ticket_id(self):
        with open(self.id_file_sem, "w") as sem:
            fcntl.flock(sem, fcntl.LOCK_EX)
            try:
                with open(self.id_file, "r+") as id_file:
                    next_id = self.increment_file(id_file)
            except FileNotFoundError: # New file, pretend it contained 1
                with open(self.id_file, "w+") as id_file:
                    print("2", file=id_file)
                    next_id = 1
        return self.format_ticket_id(next_id)

    def increment_file(self, fh):
        next_id = fh.readline()
        if next_id == "":
            next_id = 1
        else:
            next_id = int(next_id)
        fh.truncate(0)
        fh.seek(0)
        print(str(next_id + 1), file=fh)
        return next_id

    def format_ticket_id(self, id_num):
        return self.conf["id-format"].format(id_num)

    @property
    def ticket_dir(self):
        return "/home/mjd/quicket" # XXX

    @property
    def template_file(self):
        return self.config_dir / "template.md"

    @property
    def id_file(self):
        return self.config_dir / "ID"

    @property
    def id_file_sem(self):
        return self.id_file.with_suffix('.sem')
