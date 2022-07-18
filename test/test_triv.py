
import sys
sys.path.append("lib")

def test_module_load():
    from quickette.app import App
    from quickette.error import TicketParsingException
    from quickette.markdown import Markdown
    from quickette.markdown import MarkdownUtil
    from quickette.markdown import Parser
    from quickette.repo import Repository
    from quickette.ticket import Ticket
    from quickette.ticket import TicketFile
    from quickette.ticket_meta import TicketMeta
    from quickette.ticket_status import TicketStatus
