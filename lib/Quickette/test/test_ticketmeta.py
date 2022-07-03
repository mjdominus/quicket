sample_ticket="""ID: 142857
Title: sample ticket
Favorite-Food: crab cakes
Created: 2020-04-02 02:38:00
Wakeup: 2020-04-02 02:38:00
"""

from Quickette.Ticket import Ticket

def test_lines():
    t = Ticket.load_from_array(sample_ticket.splitlines())
    lns = t.header.lines()

    assert len(lns) == 5

    # order for these first three is always the same
    assert lns[0].startswith("id: ")
    assert lns[1].startswith("title: ")
    assert lns[2].startswith("created: ")

    for f in "favorite-food", "wakeup":
        assert lns[3].startswith(f"{f}: ") or lns[4].startswith(f"{f}: ")

def test___str__():
    t = Ticket.load_from_array(sample_ticket.splitlines())
    s = str(t.header)
    import sys
    print("<<" + s + ">>", file=sys.stderr)
    assert s.startswith("id: ")
    for f in "title", "favorite-food", "created", "wakeup":
        assert "\n" + f + ": " in s
