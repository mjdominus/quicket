
from Quickette.Ticket import Ticket
from datetime import datetime
import sys

sample_ticket="""ID: 142857
Title: sample ticket
Created: 2020-04-02T02:38:00
"""

def test_parse():
    print(">>", sys.version)
    t = Ticket.load_from_array(sample_ticket.splitlines())
    print("**", t.header)
    assert t.header["id"] == "142857"
    assert t.header["title"] == "sample ticket"
    assert t.header["created"] == datetime.fromisoformat("2020-04-02T02:38:00")
