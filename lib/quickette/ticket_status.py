from quickette.error import UnknownStatus

allowed = [
    "waiting to start",
    "ready",
    "in progress",
    "waiting",
    "done",
    "won't do"
    ]

class TicketStatus(str):

    default_status = "ready"

    def __init__(self, s):
        global allowed
        sl = s.lower()
        super().__init__()
        if sl not in allowed:
            raise UnknownStatus(s)

    @classmethod
    def allowed(cls):
        global allowed
        return allowed
