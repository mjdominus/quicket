
from Quickette.Ticket import Ticket
from datetime import datetime
import sys

sample_ticket="""ID: 142857
Title: sample ticket
Favorite-Food: crab cakes
Created: 2020-04-02T02:38:00
Wakeup: 2020-04-02T02:38:00
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
