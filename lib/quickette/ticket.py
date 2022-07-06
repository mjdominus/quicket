
from datetime import datetime
import os
from pathlib import Path
import sys
import re

from quickette.error import MalformedHeaderLine, MissingRequiredField, UnknownStatus

allowed = [
    "waiting to start",
    "ready",
    "in progress",
    "waiting",
    "done",
    "won't do"
    ]

class TicketStatus(str):

    default_status = "ready"

    def __init__(self, s):
        global allowed
        sl = s.lower()
        super().__init__()
        if sl not in allowed:
            raise UnknownStatus(s)

    @classmethod
    def allowed(cls):
        global allowed
        return allowed

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
    def load_from_file(cls, file):
        tf = TicketFile(file, load=True)
        return tf.ticket

    @classmethod
    def load_from_fh(cls, fh):
        lines = [ ln.rstrip() for ln in fh.readlines() ]
        if lines[-1] == "":
            lines = lines[:-1]
        return cls.load_from_array(lines)

    @classmethod
    def load_from_string(cls, s):
        return cls.load_from_array(s.splitlines())

    @classmethod
    def load_from_array(cls, lines):
        header_length = None
        for i in range(len(lines)):
            if lines[i].strip() == "":
                header_length = i
                break
        if header_length is None:
            header_length = len(lines)
            body = []
        else:
            body = lines[header_length+1 : ]

        header = TicketMeta.from_lines(lines[: header_length])

        # TODO TicketBody should be a class that supports methods like "append"
        # and maybe markdown structure
        # right now it's an array of lines
        return cls(header, body)

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


_conversions = {"created": datetime.fromisoformat,
                "status": TicketStatus,
}

# For later: make the lookup case-insensitive

class TicketMeta(dict):

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            field = k.lower().replace("_", "-")
            self[field] = v
        if "id" not in self:
            raise MissingRequiredField("id")
        if "title" not in self:
            raise MissingRequiredField("title")

        self.set_defaults()

    @classmethod
    def from_lines(cls, lines):
        fields = {}
        for line in lines:
            f, v = cls.parse_header_line(line)
            fields[f] = v
        return cls(**fields)

    @classmethod
    def conversions(cls):
        global _conversions
        return _conversions

    @classmethod
    def convert(cls, field, value_str):
        conv = cls.conversions()
        if field in conv:
            return conv[field](value_str)
        else:
            return value_str

    def set_defaults(self):
        self.set_default_created()
        self.set_default_status()

    def set_default_created(self):
        if "created" not in self:
            self["created"] = datetime.now()

    def set_default_status(self):
        if "status" not in self:
            self["status"] = TicketStatus.default_status

    # XXX Unicode
    @classmethod
    def parse_header_line(cls, line):
        m = re.match(r'([a-zA-Z_][a-zA-Z_0-9-]*):\s+(.*)', line)
        if m:
            f, v = m.groups()
            f = f.lower()
            return f, cls.convert(f, v)
        else:
            raise MalformedHeaderLine(line)

    def field_line(self, field, newline=False):
        s = f"{field}: {self[field]}"
        if newline:
            s += "\n"
        return s

    def lines(self):
        lns = []
        # These come first
        top = [ "id", "title", "status", "created" ]
        for f in top:
            lns.append(self.field_line(f))
        for f in self.keys():
            if f in top:
                continue
            if self[f] is not None:
                lns.append(self.field_line(f))
        return lns

    def __str__(self):
        return "\n".join(self.lines() + [""])

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
