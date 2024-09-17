import re


class CommandRelatedTicket:
    # This summary is used for the user documentation
    """Add to the current ticket a relationship to another ticket. Supports all ticket 
relations: blocked by, blocks and related.
The command keywords are `relate`, `blocks` and `blocked_by` along with the ticket
reference, i.e. `#<ticket-number>`.

Valid commands are as follows:

- /relate #1

- /blocks #1

- /blocked_by #1

For this command to process the following conditions must be met:

- There is either a `<new line>` (`\\n`) or a `<space>` char immediatly before the slash `/`

- There is a `<space>` char after the command keyword, i.e. `/relate<space>#1`
"""


    related_ticket: str = r'[\s|\n]\/(?P<command>[relate|blocks|blocked_by]+)\s\#(?P<ticket>\d+)[\s|\n]?'


    def command_related_ticket(self, match) -> str:
        """/relate, /blocks and /blocked_by processor

        Slash command usage within a ticket description will add an action comment with the
        time spent. For a ticket comment, it's duration field is set to the duration valuee calculated.

        Args:
            match (re.Match): Named group matches

        Returns:
            str: The matched string if the duration calculation is `0`
            None: On successfully processing the command
        """

        a = 'a'

        command = match.group('command')
        ticket_id:int =  str(match.group('ticket'))

        if ticket_id is not None:

            from core.models.ticket.ticket import RelatedTickets

            if command == 'relate':

                how_related = RelatedTickets.Related.RELATED.value

            elif command == 'blocks':

                how_related = RelatedTickets.Related.BLOCKS.value

            elif command == 'blocked_by':

                how_related = RelatedTickets.Related.BLOCKED_BY.value

            else:

                #ToDo: Add logging that the slash command could not be processed.

                return str(match.string[match.start():match.end()])


            if str(self._meta.verbose_name).lower() == 'ticket':

                from_ticket = self

                to_ticket = self.__class__.objects.get(pk = ticket_id)

            elif str(self._meta.verbose_name).lower() == 'comment':

                from_ticket = self.ticket

                to_ticket = self.ticket.__class__.objects.get(pk = ticket_id)


            RelatedTickets.objects.create(
                from_ticket_id = from_ticket,
                how_related = how_related,
                to_ticket_id = to_ticket,
                organization = self.organization
            )

        else:

            #ToDo: Add logging that the slash command could not be processed.

            return str(match.string[match.start():match.end()])

        return None
