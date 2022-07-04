
from quickette.ticket import Ticket, TicketMeta
from datetime import datetime
import pytest
import sys

sample_ticket="""ID: 142857
Title: sample ticket
Favorite-Food: crab cakes
Created: 2020-04-02 02:38:00
Wakeup: 2020-04-02 02:38:00

I am a ticket body
"""

def test_parse():
    t = Ticket.load_from_array(sample_ticket.splitlines())

    # lowercasing of field names
    assert t.header["id"] == "142857"
    assert t.header["title"] == "sample ticket"

    # conversions
    assert t.header["created"] == datetime.fromisoformat("2020-04-02T02:38:00")

    # Hyphens in the key, spaces in the value
    assert t.header["favorite-food"] == "crab cakes"

    with pytest.raises(KeyError):
        t.header["poo"]

    assert t.body == [ "I am a ticket body" ]

def test___str__():
    # Also tests Ticket.load_from_string and round-tripping of dump-then-parse
    t1 = Ticket.load_from_array(sample_ticket.splitlines())
    t2 = Ticket.load_from_string(str(t1))

    assert str(t2) == str(t1)

def test_no_body():
    t1 = Ticket(TicketMeta(id=1, title="foo"))
    assert t1.body == ""
