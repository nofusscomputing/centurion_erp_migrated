import re

from markdown_it import MarkdownIt

from mdit_py_plugins import admon, footnote, tasklists

from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name

from django.template.loader import render_to_string



class TicketMarkdown:
    """Ticket and Comment markdown functions
    
    Intended to be used for all areas of a tickets, projects and comments.
    """


    def highlight_func(self, code: str, lang: str, _) -> str | None:
        """Use pygments for code high lighting"""

        if not lang:

            return None

        lexer = get_lexer_by_name(lang)

        formatter = HtmlFormatter(style='vs', cssclass='codehilite')

        return highlight(code, lexer, formatter)


    def render_markdown(self, markdown_text):
        """Render Markdown

        implemented using https://markdown-it-py.readthedocs.io/en/latest/index.html

        Args:
            markdown_text (str): Markdown text

        Returns:
            str: HTML text
        """

        markdown_text = self.ticket_reference(markdown_text)

        md = (
            MarkdownIt(
                config = "commonmark",
                options_update={
                    'linkify': True,
                    'highlight': self.highlight_func
                }
            )

            .enable([
                'linkify',
                'strikethrough',
                'table',
            ])

            .use(admon.admon_plugin)
            .use(footnote.footnote_plugin)
        )

        return md.render(markdown_text)


    def build_ticket_html(self, match):

        ticket_id = match.group(1)

        if hasattr(self, 'ticket'):

            ticket = self.ticket.__class__.objects.get(pk=ticket_id)

        else:

            ticket = self.__class__.objects.get(pk=ticket_id)

        project_id = str('0')

        if ticket.project:

            project_id = str(ticket.project.id).lower()

        context: dict = {
            'id': ticket.id,
            'name': ticket,
            'ticket_type': str(ticket.get_ticket_type_display()).lower(),
            'ticket_status': str(ticket.get_status_display()).lower(),
            'project_id': project_id,
        }

        html_link = render_to_string('core/ticket/renderers/ticket_link.html.j2', context)

        return str(html_link)



    def ticket_reference(self, text):

        return re.sub('#(\d+)', self.build_ticket_html, text)