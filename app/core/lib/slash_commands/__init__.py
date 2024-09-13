import re

from .duration import Duration


class SlashCommands(
    Duration
):
    """Slash Commands Base Class
    
    This class in intended to be included in the following models:
    
    - Ticket
    
    - TicketComment
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

        return markdown
