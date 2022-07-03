
from Quickette.Error import UnknownStatusException

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
            raise UnknownStatusException(s)

    @classmethod
    def allowed(cls):
        global allowed
        return allowed
