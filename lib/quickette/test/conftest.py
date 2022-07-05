
import pytest

@pytest.fixture
def sample_ticket_text():
    return """ID: 142857
Title: sample ticket
Created: 2020-04-02 02:38:00
Favorite-Food: crab cakes
Status: ready

This is a ticket body.

It has two sections.
"""

@pytest.fixture
def sample_ticket_2_text():
    return """ID: 285741
Title: sample sub ticket
Created: 2020-04-03 14:22:00

I am a sub ticket of the first ticket
"""


@pytest.fixture
def ticketdir(tmpdir, sample_ticket_text):
    top = tmpdir / "top.md"
    top.write_text(sample_ticket_test)

    bot = tmpdir / "top.d" / "bot.md"
    bot.write_text(sample_ticket_2_test)

    return tmpdir
