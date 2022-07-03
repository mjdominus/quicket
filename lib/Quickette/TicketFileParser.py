
import sys
from TicketMeta import TicketMeta

fields = { "title": None,
           "id": "",
           "created": datetime,
           "lastactivity": datetime,
           "status": status,
           "wakeup": datetime,
           "tags": taglist,
}


class TicketHeaderParser():
    def __init__(self, ticket_meta_class=TicketMeta):
        self.meta_class = ticket_meta_class

    def parse_lines(self, lines)
        for line in lines:
            field, value = self.split_header_line(line)
            field = self.normalize_field_name(field)

    def split_header_line(self, line):
        f, v = line.partition(":")
        return f, v.lstrip()

    def normalize_field_name(self, fieldname):
        return fieldname.strip().lower().replace("-", "")
