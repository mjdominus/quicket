
import pytest

from Quickette.TicketStatus import TicketStatus
from Quickette.Error import UnknownStatusException

def test_basic():
    assert TicketStatus("ready to start")
    assert TicketStatus("in progress")
    assert TicketStatus("done")

    with pytest.raises(UnknownStatusException):
        TicketStatus("poo")

    # __str__ and lowercasing
    z = str(TicketStatus("Done")) == "done"
