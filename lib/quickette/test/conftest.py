
import pytest
from pathlib import Path

@pytest.fixture
def sample_ticket_text():
    return """# sample ticket

* ID: 142857
* Created: 2020-04-02 02:38:00
* Favorite-Food: crab cakes
* Status: ready

This is a ticket body.

It has two sections.
"""

@pytest.fixture
def sample_ticket_2_text():
    return """# sample sub ticket

* ID: 285741
* Created: 2020-04-03 14:22:00

I am a sub ticket of the first ticket
"""

# A ticket that has a subticket
@pytest.fixture
def ticketpair(tmpdir, sample_ticket_text, sample_ticket_2_text):
    top = tmpdir / "top.md"
    top.write_text(sample_ticket_text, encoding='utf8')

    bot = tmpdir / "top.d" / "bot.md"
    Path(bot).parent.mkdir(parents=True, exist_ok=True)
    bot.write_text(sample_ticket_2_text, encoding='utf8')

    return top, bot
