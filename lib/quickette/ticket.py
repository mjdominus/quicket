
from datetime import datetime
import os
import sys
import re

from quickette.error import MalformedHeaderLine, MissingRequiredField, UnknownStatus

allowed = [
    "waiting to start",
    "ready to start",
    "in progress",
    "waiting",
    "done",
    "won't do"
    ]

class TicketStatus(str):

    default_status = "ready to start"

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

    @classmethod
    def load_from_file(cls, file):
        with open(file) as fh:
            return cls.load_from_fh(fh)

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

    def __str__(self):
        return str(self.header) + "\n" + "\n".join(self.body) + "\n"


_conversions = {"created": datetime.fromisoformat,
                "status": TicketStatus,
}

# For later: make the lookup case-insensitive

class TicketMeta(dict):

    def __init__(self, **kwargs):

        for k, v in kwargs.items():
            self[k] = v
        if "id" not in kwargs:
            raise MissingRequiredField("id")
        if "title" not in kwargs:
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
            raise MalformedHeaderLineException(line)

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
