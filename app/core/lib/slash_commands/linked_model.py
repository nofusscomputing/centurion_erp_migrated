import re



class CommandLinkedModel:
    # This summary is used for the user documentation
    """Link an item to the current ticket. Supports all ticket 
relations: blocked by, blocks and related.
The command keyword is `link` along with the model reference, i.e. `$<type>-<number>`.

Valid commands are as follows:

- /link $device-1

- /link $cluster-55

Available model types for linking are as follows:

- cluster

- config_group

- device

- operating_system

- service

- software

For this command to process the following conditions must be met:

- There is either a `<new line>` (`\\n`) or a `<space>` char immediatly before the slash `/`

- There is a `<space>` char after the command keyword, i.e. `/link<space>$device-101`
"""


    linked_item: str = r'[\s|\n]\/(?P<command>[link]+)\s\$(?P<type>[a-z_]+)-(?P<id>\d+)[\s|\n]?'


    def command_linked_model(self, match) -> str:
        """/link processor

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

        model_type:int =  str(match.group('type'))
        model_id:int =  int(match.group('id'))


        try:

            from core.models.ticket.ticket_linked_items import TicketLinkedItem

            if model_type == 'cluster':

                from itim.models.clusters import Cluster

                model = Cluster

                item_type = TicketLinkedItem.Modules.CLUSTER

            elif model_type == 'config_group':

                from config_management.models.groups import ConfigGroups

                model = ConfigGroups

                item_type = TicketLinkedItem.Modules.CONFIG_GROUP

            elif model_type == 'device':

                from itam.models.device import Device

                model = Device

                item_type = TicketLinkedItem.Modules.DEVICE

            elif  model_type == 'operating_system':

                from itam.models.operating_system import OperatingSystem

                model = OperatingSystem

                item_type = TicketLinkedItem.Modules.OPERATING_SYSTEM

            elif model_type == 'service':

                from itim.models.services import Service

                model = Service

                item_type = TicketLinkedItem.Modules.SERVICE

            elif model_type == 'software':

                from itam.models.software import Software

                model = Software

                item_type = TicketLinkedItem.Modules.SOFTWARE

            else:

                return str(match.string[match.start():match.end()])


            if str(self._meta.verbose_name).lower() == 'ticket':

                ticket = self

            elif str(self._meta.verbose_name).lower() == 'ticket comment':

                ticket = self.ticket


            if model:

                item = model.objects.get(
                    pk = model_id
                )

                from core.serializers.ticket_linked_item import TicketLinkedItemModelSerializer

                serializer = TicketLinkedItemModelSerializer(
                    data = {
                        'organization': ticket.organization,
                        'ticket': ticket.id,
                        'item_type': item_type,
                        'item': item.id
                    }
                )

                if serializer.is_valid():

                    serializer.save()

                    return None

                return str(match.string[match.start():match.end()])

        except Exception as e:

            return str(match.string[match.start():match.end()])

        return None
