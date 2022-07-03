
import sys
from Quickette.TicketMeta import TicketMeta

class Ticket():
    def __init__(self, header, body):
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
