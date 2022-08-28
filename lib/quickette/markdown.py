
from quickette.ticket_meta import TicketMeta
from quickette.error import MissingTitle
from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode

class Parser():
    def __init__(self):
        self.markdown_it = MarkdownIt()

    def parse(self, target):
        tokens = self.markdown_it.parse(target)
        return SyntaxTreeNode(tokens)

class Markdown():
    """
    Glue class that translates between Quickette's idea of Markdown
    and whatever underlying package that actually understands Markdown.
    At present the underlying class is [`markdown-it`](https://markdown-it-py.readthedocs.io/en/latest/api/markdown_it.html).
    """
    def __init__(self, md):
        """
        `md` here is intended to be a representation of the markdown that is
        selected for ease of manipulation.  In the original implementation
        it will be the tree structure returned by markdown_it.tree.SyntaxTreeNode
        """

        assert type(md) == SyntaxTreeNode
        assert md.is_root
        self.md = md

    @classmethod
    def parser(cls):
        return MarkdownIt()

    def find_text(self, node=None):
        """
        Walk given piece of Markdown and return a list of the texts found

        Default: walk entire Markdown represented by self
        """
        if node is None:
            node = self.md
        return [ n.content for n in node.walk() if n.type == "text" ]

    def split_markdown(self):
        """
        Given the markdown representation of the entire document, break it into parts:

        TODO ??? XXX
        """

        result = {}
        children = self.md.children
        assert


    def header(self):
        """
        Return a representation of the markdown that contains the ticket's title
        and metadata
        """
        md = self.md
        import pdb
        pdb.set_trace()

        title = md.children[0]
        assert title.type == "heading"
        title_texts = self.find_text(title)
        assert len(title_texts) == 1
        title_text = title_texts[0]

        metadata = md.children[1]
        assert metadata.type == "bullet_list"
        meta_texts = self.find_text(metadata)
        meta = TicketMeta.from_lines(meta_texts, title=title_text)

        return meta


    def body(self):
        """
        Return a representation of the markdown that contains the ticket's body
        """
        md = self.md
        children = list(md.children)[2:]
        return


class MarkdownUtil():
    def __init__(self):
        pass

    def warning(self, m):
        print("MarkdownUtil warning:", m, file=sys.stderr)

    def find_title(self, md):
        raise Exception("Unimplemented")
        if md.get_type() != 'Document':
            raise MissingTitle("Markdown element is not a Document")
        for c in md.children():
            t = c.get_type()
            if t == "BlankLine":
                continue
            elif t == "Heading":
                if c.level != 1:
                    self.warning(f"Found title in level {c.level} heading; expected level 1")
                return c
            else:
                raise MissingTitle(f"Found element of type {t} at start of document; expected Heading")

    def find_header(self, md):
        raise Exception("Unimplemented")
        if md.get_type() != 'Document':
            raise MissingHeader("Markdown element is not a Document")
        title = self.find_title(md)
        for c in md.children():
            t = c.get_type()
            if t == "BlankLine" or c == title:
                continue
            elif t == "List":
                if c.ordered:
                    self.warning(f"Found metadata list but it was an ordered list; expected unordered");
                return c
            else:
                raise MissingHeader(f"Found element of type {t} instead of ticket metadata; expected List")
