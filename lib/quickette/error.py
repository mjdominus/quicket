
class TicketParsingException(Exception):
    pass

class MalformedHeaderLine(TicketParsingException):
    pass

class UnknownStatus(ValueError):
    pass

class MissingRequiredField(ValueError):
    pass
