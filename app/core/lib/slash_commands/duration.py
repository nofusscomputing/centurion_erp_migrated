import re


class Duration:
    # This summary is used for the user documentation
    """The command keyword is `spend` and you can also use `spent`. The formatting for the time
after the command, is `<digit>` then either `h`, `m`, `s` for hours, minutes and seconds respectively.

Valid commands are as follows:

- /spend 1h1ms

- /spend 1h 1m 1s

For this command to process the following conditions must be met:

- There is either a `<new line>` (`\\n`) or a `<space>` char immediatly before the slash `/`

- There is a `<space>` char after the command keyword, i.e. `/spend<space>1h`

- _Optional_ `<space>` char between the time blocks.
"""


    time_spent: str = r'[\s|\n]\/(?P<command>[spend|spent]+)\s(?P<time>(?P<hours>\d+h)?\s?(?P<minutes>[\d]{1,2}m)?\s?(?P<seconds>\d+[s])?)[\s|\n]?'


    def command_duration(self, match) -> str:
        """/spend, /spent processor

        Slash command usage within a ticket description will add an action comment with the
        time spent. For a ticket comment, it's duration field is set to the duration valuee calculated.

        Args:
            match (re.Match): Grouped matches

        Returns:
            str: The matched string if the duration calculation is `0`
            None: On successfully processing the command
        """

        a = 'a'

        command = match.group('command')
        time:str =  str(match.group('time')).replace(' ', '')
        hours =  match.group('hours')
        minutes =  match.group('minutes')
        seconds =  match.group('seconds')

        duration: int = 0

        if hours is not None:

            duration += int(hours[:-1])*60*60

        if minutes is not None:

            duration += int(minutes[:-1])*60

        if seconds is not None:

            duration += int(seconds[:-1])

        if duration > 0:

            if str(self._meta.verbose_name).lower() == 'ticket':

                from core.models.ticket.ticket_comment import TicketComment

                comment_text = f'added {time} of time spent'

                TicketComment.objects.create(
                    ticket = self,
                    comment_type = TicketComment.CommentType.ACTION,
                    body = comment_text,
                    duration = duration,
                    user = self.opened_by,
                )

            if str(self._meta.verbose_name).lower() == 'comment':

                self.duration = duration

        else:

            #ToDo: Add logging that the slash command could not be processed.

            return str(match.string[match.start():match.end()])

        return None
