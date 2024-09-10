import markdown as md
import re

from django.template.loader import render_to_string

class TicketMarkdown:
    """Ticket and Comment markdown functions
    
    Intended to be used for all areas of a tickets, projects and comments.
    """


    def render_markdown(self, markdown_text):

        markdown_text = self.ticket_reference(markdown_text)

        return md.markdown(markdown_text, extensions=['markdown.extensions.fenced_code', 'codehilite'])


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