
class TicketParsingException(Exception):
    pass

class MalformedHeaderLineException(TicketParsingException):
    pass

class UnknownStatusException(ValueError):
    pass

class MissingRequiredField(ValueError):
    pass
