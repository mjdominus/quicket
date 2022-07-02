
class TicketParsingException(Exception):
    pass

class MalformedHeaderLineException(TicketParsingException):
    pass
