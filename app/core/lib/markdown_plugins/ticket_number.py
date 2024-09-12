
import re

from django.template.loader import render_to_string

from markdown_it import MarkdownIt
from markdown_it.rules_core import StateCore
from markdown_it.token import Token

# Regex string to match a whitespace character, as specified in
# https://github.github.com/gfm/#whitespace-character
# (spec version 0.29-gfm (2019-04-06))
_GFM_WHITESPACE_RE = r"[ \t\n\v\f\r]"


def plugin(
    md: MarkdownIt,
    enabled: bool = False,
) -> None:
    """markdown_it plugin to render ticket numbers

    Placing `#<number>` within markdown will be rendered as a pretty link to the ticket.

    Args:
        md (MarkdownIt): markdown object
        enabled (bool, optional): Enable the parsing of ticket references. Defaults to False.

    Returns:
        None: nada
    """

    def main(state: StateCore) -> None:
       
        tokens = state.tokens
        for i in range(0, len(tokens) - 1):
            if is_tag_item(tokens, i):
                tag_render(tokens[i])


    def is_inline(token: Token) -> bool:
        return token.type == "inline"


    def is_tag_item(tokens: list[Token], index: int) -> bool:

        return (
            is_inline(tokens[index])
            and contains_tag_item(tokens[index])
        )


    def tag_html(match):

        ticket_id = match.group(1)

        try:
            from core.models.ticket.ticket import Ticket

            ticket = Ticket.objects.get(pk=ticket_id)

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

            return html_link
        except:

            return str('#' + ticket_id)


    def tag_render(token: Token) -> None:
        assert token.children is not None

        checkbox = Token("html_inline", "", 0)

        checkbox.content = tag_replace(token.content)

        token.children[0] = checkbox


    def tag_replace(text):

        return re.sub('#(\d+)', tag_html, text)

    def contains_tag_item(token: Token) -> bool:

        return re.match(rf"(.+)?#(\d+){_GFM_WHITESPACE_RE}?(.+)?", token.content) is not None

    if enabled:

        md.core.ruler.after("inline", "links", fn=main)
