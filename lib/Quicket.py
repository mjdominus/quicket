
from pathlib import Path

class Quicket():
    def __init__(self, config_dir=None):
        if config_dir is None:
            config_dir = "/home/mjd/.quicket" # XXX should default to $HOME/.quicket
        self.config_dir = Path(config_dir)

    @property
    def ticket_dir(self):
        return "/home/mjd/quicket" # XXX

    @property
    def template_file(self):
        return self.config_dir / "template.md"
