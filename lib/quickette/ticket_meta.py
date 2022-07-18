# For later: make the lookup case-insensitive
from datetime import datetime
import re
from quickette.error import MalformedHeaderLine, MissingRequiredField
from quickette.ticket_status import TicketStatus


_conversions = {"created": datetime.fromisoformat,
                "status": TicketStatus,
}

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
    def from_lines(cls, lines, **kwargs):
        import pdb
        pdb.set_trace()
        fields = {}
        for line in lines:
            f, v = cls.parse_header_line(line)
            fields[f] = v
        for f, v in kwargs.items():
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
