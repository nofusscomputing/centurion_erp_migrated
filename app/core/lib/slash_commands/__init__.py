import re

from .duration import Duration
from .related_ticket import CommandRelatedTicket
from .linked_model import CommandLinkedModel


class SlashCommands(
    Duration,
    CommandRelatedTicket,
    CommandLinkedModel,
):
    """Slash Commands Base Class
    
    This class in intended to be included in the following models:
    
    - Ticket
    
    - TicketComment

    Testing of regex can be done at https://pythex.org/
    """


    def slash_command(self, markdown:str) -> str:
        """ Slash Commands Processor

        Markdown text that contains a slash command is passed to this function and on the processing
        of any valid slash command, the slash command will be removed from the markdown.

        If any error occurs when attempting to process the slash command, it will not be removed from
        the markdown. This is by design so that the "errored" slash command can be inspected.

        Args:
            markdown (str): un-processed Markdown

        Returns:
            str: Markdown without the slash command text.
        """

        markdown = re.sub(self.time_spent, self.command_duration, markdown)

        markdown = re.sub(self.linked_item, self.command_linked_model, markdown)

        markdown = re.sub(self.related_ticket, self.command_related_ticket, markdown)

        return markdown
