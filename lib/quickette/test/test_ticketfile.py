
from quickette.ticket import Ticket, TicketFile
import pytest

@pytest.mark.skip("Haven't written subticket feature yet")
def test_subtickets():
    pass

def test_basic(tmpdir, sample_ticket_text):
    fn = tmpdir / "basic.md"
    fn.write_text(sample_ticket_text, encoding="utf8")

    tf = TicketFile(fn)
    assert tf.loaded
    assert tf.header["title"] == "sample ticket"
    assert len(tf.body) == 3
    assert "two sections" in tf.body[-1]

    assert tf.ticket is not None
    assert tf.ticket.file == tf

    tf0 = TicketFile(fn, load=False)
    assert not tf0.loaded
    assert "ticket" not in tf0.__dict__ or tf0.__dict__["ticket"] is None

def test_update(tmpdir, sample_ticket_text):
    fn = tmpdir / "update.md"

    fn.write_text(sample_ticket_text, encoding="utf8")
    tf = TicketFile(fn)
    tf.ticket.body = tf.body + [ "", "No, I meant three sections" ]
    tf.header["favorite-food"] = "crab cakes"
    tf.header["title"] = "dummy ticket"

    tf.update()

    tf2 = TicketFile(fn)
    assert tf2.header["title"] == "dummy ticket"
    assert tf2.header["favorite-food"] == "crab cakes"
    assert len(tf2.body) == 5
    assert "three sections" in tf2.body[-1]

def test_load_ticket_with_subticket(ticketpair):
    top_path, _ = ticketpair
    top = Ticket.load_from_file(top_path)
    assert len(top.subtickets) == 1

    bot = list(top.subtickets)[0]
    assert bot.parent == top
