
import pytest

from quickette.ticket_status import TicketStatus
from quickette.error import UnknownStatus

def test_basic():
    assert TicketStatus("ready")
    assert TicketStatus("in progress")
    assert TicketStatus("done")

    with pytest.raises(UnknownStatus):
        TicketStatus("poo")

    # __str__ and lowercasing
    z = str(TicketStatus("Done")) == "done"
