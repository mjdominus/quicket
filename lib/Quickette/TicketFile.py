
from Quickette.Ticket import Ticket
import os

# Read-only for now; later add file locking
class TicketFile():
    def __init__(self, filename, load=True):
        self.filename = filename
        self.tmp = filename + ".tmp"
        self.loaded = False
        if load:
            self.load()

    def load(self):
        if self.loaded:
            return
        with open(self.filename) as fh:
            self.ticket = Ticket.load_from_fh(fh)
        self.loaded = True

    def update(self):
        if not self.loaded:
            return

        # Todo: semaphore
        with open(self.tmp, "w") as fh:
            print(str(self.ticket), file=fh)
        os.rename(self.tmp, self.filename)

    @property
    def header(self):
        return self.ticket.header

    @property
    def body(self):
        return self.ticket.body
