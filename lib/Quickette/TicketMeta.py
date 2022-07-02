
from datetime import datetime
import sys
import re

from Quickette.Error import MalformedHeaderLineException

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
