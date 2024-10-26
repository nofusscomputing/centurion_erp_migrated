from api.exceptions import UnknownTicketType
from api.viewsets.common import ModelViewSet

from assistance.serializers.request import (
    RequestAddTicketModelSerializer,
    RequestChangeTicketModelSerializer,
    RequestTriageTicketModelSerializer,
    RequestImportTicketModelSerializer,
    RequestTicketModelSerializer,
    RequestTicketViewSerializer
)
from core.serializers.ticket import (
    Ticket,
)

from settings.models.user_settings import UserSettings


class TicketViewSet(ModelViewSet):

    filterset_fields = [
        'category',
        'external_system',
        'impact',
        'milestone',
        'organization',
        'priority',
        'project',
        'status',
        'urgency',
    ]

    search_fields = [
        'title',
        'description',
    ]

    model = Ticket

    _ticket_type_id: int = None

    _ticket_type: str = None
    """Name for type of ticket

    String is Camel Cased.
    """


    def get_queryset(self):

        self.get_ticket_type()

        queryset = super().get_queryset().filter(
            ticket_type = self._ticket_type_id
        )

        self.queryset = queryset

        return self.queryset


    def get_ticket_type(self) -> None:

        ticket_type_id: int = None

        if self._ticket_type_id is None:

            ticket_types = [e for e in Ticket.TicketType]

            for i in range( 1, len(ticket_types) ):

                if self._ticket_type.lower() == str(ticket_types[i - 1].label).lower():

                    ticket_type_id = i

                    break

            self._ticket_type_id = ticket_type_id


        if self._ticket_type_id is None:

            raise UnknownTicketType()


    def get_serializer_class(self):

        serializer_prefix:str = None

        self.get_ticket_type()

        serializer_prefix = self._ticket_type


        if (
            self.action == 'create'
            or self.action == 'list'
        ):


            if (
                self.action == 'create'
                or self.action == 'list'
            ):

                user_settings = UserSettings.objects.get(
                    user = self.request.user
                )

                organization = user_settings.default_organization.id


            if (
                self.action == 'create'
            ):

                if self.request.data is not None:

                    if 'organization' in self.request.data:

                        organization = int(self.request.data['organization'])


            if (    # Must be first as the priority to pickup
                self._ticket_type
                and self.action != 'list'
                and self.action != 'retrieve'
            ):


                if self.has_organization_permission(
                    organization = organization,
                    permissions_required = [
                        'core.import_ticket_request'
                    ]
                ):

                    serializer_prefix = self._ticket_type + 'Import'

                elif self.has_organization_permission(
                    organization = organization,
                    permissions_required = [
                        'core.triage_ticket_request'
                    ]
                ):

                    serializer_prefix = self._ticket_type + 'Triage'

                elif self.has_organization_permission(
                    organization = organization,
                    permissions_required = [
                        'core.change_ticket_request'
                    ]
                ):

                    serializer_prefix = self._ticket_type + 'Change'

                elif self.has_organization_permission(
                    organization = organization,
                    permissions_required = [
                        'core.add_ticket_request'
                    ]
                ):

                    serializer_prefix = self._ticket_type + 'Add'

                elif self.has_organization_permission(
                    organization = organization,
                    permissions_required = [
                        'core.view_ticket_request'
                    ]
                ):

                    serializer_prefix = self._ticket_type + 'View'



        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()[serializer_prefix + 'TicketViewSerializer']


        return globals()[serializer_prefix + 'TicketModelSerializer']
