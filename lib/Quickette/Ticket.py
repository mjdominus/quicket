
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
        lines = fh.getlines()
        return cls.load_from_array(lines)

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

        header = TicketMeta(lines[: header_length])
        return cls(header, body)
