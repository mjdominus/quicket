
from datetime import datetime
import sys
import re

from Quickette.Error import MalformedHeaderLineException

# For later: make the lookup case-insensitive

class TicketMeta(dict):
    def __init__(self, lines):
        self.conversions = {"created": datetime.fromisoformat}
        for line in lines:
            f, v = self.parse_header_line(line)
            self[f] = v

    def convert(self, field, value_str):
        if field in self.conversions:
            return self.conversions[field](value_str)
        else:
            return value_str

    # XXX Unicode
    def parse_header_line(self, line):
        m = re.match(r'([a-zA-Z_][a-zA-Z_0-9-]*):\s+(.*)', line)
        if m:
            f, v = m.groups()
            f = f.lower()
            return f, self.convert(f, v)
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
        top = [ "id", "title", "created" ]
        for f in top:
            lns.append(self.field_line(f))
        for f in self.keys():
            if f in top:
                continue
            lns.append(self.field_line(f))
        return lns

    def __str__(self):
        return "\n".join(self.lines() + [""])
