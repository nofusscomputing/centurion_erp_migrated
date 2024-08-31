import markdown as md


class TicketMarkdown:
    """Ticket and Comment markdown functions
    
    Intended to be used for all areas of a tickets, projects and comments.
    """


    def render_markdown(self, markdown_text):



        return md.markdown(markdown_text, extensions=['markdown.extensions.fenced_code', 'codehilite'])
