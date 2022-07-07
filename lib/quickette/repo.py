
import contextlib
import fcntl
import os
from pathlib import Path
import sys
import toml

class Repository():
    def __init__(self, repo_rootdir, create=False):
        self.rootdir = Path(repo_rootdir)

        if create:
            self.create_repo()

        self.reload_configuration()
        self.config = self.default_config()

    def create_repo(self):
        self.config_dir().mkdir(parents=True, exist_ok=True)
        with self.main_config_file().open("x") as fh:
            toml.dump(self.default_config(), fh)

    def default_config(self):
        return { "id-format": "{}" }

    def config_dir(self):
        return self.rootdir / ".config"

    def config_file(self, filename):
        return self.config_dir() / filename

    def id_file(self):
        return self.config_file("last_id")

    def sem_file(self):
        return self.config_file("last_id.sem")

    def main_config_file(self):
        return self.config_file("main")

    def allocate_ticket_id(self):
        with open(self.sem_file(), "w") as sem:
            fcntl.flock(sem, fcntl.LOCK_EX)
            try:
                with open(self.id_file(), "r+") as id_file:
                    next_id = self.increment_file(id_file)
            except FileNotFoundError: # New file, pretend it contained 1
                with open(self.id_file(), "w+") as id_file:
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
        return self.config["id-format"].format(id_num)

    def reload_configuration(self):
        config = self.default_config()

        with open(self.main_config_file()) as fh:
            for k, v in toml.load(fh).items():
                config[k] = v

        self.config = config
