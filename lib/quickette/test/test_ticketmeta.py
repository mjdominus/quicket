

from quickette.ticket import Ticket, TicketMeta

import pytest

sample_ticket="""ID: 142857
Title: sample ticket
Favorite-Food: crab cakes
Created: 2020-04-02 02:38:00
Wakeup: 2020-04-02 02:38:00
"""


def test_lines():
    t = Ticket.load_from_array(sample_ticket.splitlines())
    lns = t.header.lines()

    assert len(lns) == 6 # status was inserted automatically

    # order for these first three is always the same
    assert lns[0].startswith("id: ")
    assert lns[1].startswith("title: ")
    assert lns[2] == "status: ready" # inserted automatically
    assert lns[3].startswith("created: ")

    for f in "favorite-food", "wakeup":
        assert lns[4].startswith(f"{f}: ") or lns[5].startswith(f"{f}: ")

def test___str__():
    t = Ticket.load_from_array(sample_ticket.splitlines())
    s = str(t.header)
    assert s.startswith("id: ")
    for f in "title", "favorite-food", "created", "wakeup", "status":
        assert "\n" + f + ": " in s

def test_defaults():
    t = TicketMeta(id="foo", title="dummy")
    assert str(t["status"]) == "ready"
    assert "created" in t

# Make sure kwargs are converted to lowercase
# and underscores turn into hyphens
def test_transform_attribute():
    tm = TicketMeta(ID=1, Title="foo", Created="1234", favorite_food="crab cakes")
    assert tm["id"] == 1
    assert tm["title"] == "foo"
    assert tm["created"] == "1234"
    assert tm["favorite-food"] == "crab cakes"


# Make sure None fields are omitted from the output
@pytest.mark.xfail
def test__none__():
    raise Exception("Didn't write this yet")
