
import os
from pathlib import Path
import sys
import re

from quickette.markdown import Markdown, Parser

class Ticket():
    # TODO: Maybe __init__(self, body, **kwargs)
    #       is a shortcut for __init__(self, TicketHeader(**kwargs), body)
    def __init__(self, header, body=""):
        self.header = header
        self.body = body
        self.subtickets = set()
        self.parent = None
        self.file = None

    @classmethod
    def default_parser(cls):
        return Parser()

    @classmethod
    def load_from_file(cls, file, parser=None):
        tf = TicketFile(file, load=True)
        return tf.ticket

    @classmethod
    def load_from_fh(cls, fh, parser=None):
        # markdown-it doesn't have a parse-from-fh option so
        # we will read it into a string
        return cls.load_from_string(fh.read(), parser=parser)

    @classmethod
    def load_from_string(cls, s, parser=None):
        if parser is None:
            parser = cls.default_parser()
        return cls.load_from_markdown(parser.parse(s))

    @classmethod
    def load_from_array(cls, lines):
        return cls.load_from_string("".join(lines))

    @classmethod
    def load_from_markdown(cls, md_obj):
         md = Markdown(md_obj)
         ticket = cls(md.header(), md.body())
         ticket.markdown = md
         return ticket

    @property
    def title(self):
        return self.header.title

    def add_subticket(self, *subtickets):
        for st in subtickets:
            self.subtickets.add(st)
            st.parent = self

    def all_subtickets(self):
        result = set([ self ])
        for t in self.subtickets:
            result |= t.all_subtickets()
        return result

    def root(self):
        while self.parent is not None:
            self = self.parent
        return self

    def relatives(self):
        return self.root().all_subtickets()

    def save(self, filename=None):
        if self.filename is None:
            if filename is None:
                self.filename = self.generate_filename(self.title)
            else:
                self.filename = filename
        pass # TODO

    @classmethod
    def generate_filename(cls, title):
        # No filename was supplied for this ticket, so make one
        # up based on the title
        # XXX
        basename = title.lower()  # Do I really want this?
        basename = re.sub(r'\s+', "-", basename)
        basename = re.sub(r'[^\w-]', "", basename)
        basename += ".md"
        return basename

    def __str__(self):
        return str(self.header) + "\n" + "\n".join(self.body) + "\n"


# Read-only for now; later add file locking
class TicketFile():
    def __init__(self, filename, load=True):
        filename = Path(filename)
        self.filename = filename
        self.tmp = filename.with_name(filename.name + ".tmp")
        self.loaded = False
        if load:
            self.load()

    def load(self):
        if self.loaded:
            return
        with self.filename.open() as fh:
            self.ticket = Ticket.load_from_fh(fh)
            self.ticket.file = self

        for subticket in self.ingest_subtickets():
            self.ticket.add_subticket(subticket)

        self.loaded = True

    def ingest_subtickets(self):
        subtickets = []

        d = self.subticket_dir_name()
        if not d.exists():
            print("**", d, "does not exist", file=sys.stderr)
            return []

        for entry in d.iterdir():
            if entry.is_file:
                subtickets.append(Ticket.load_from_file(entry))
        return subtickets

    def subticket_dir_name(self):
        return self.filename.with_suffix(".d")

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
