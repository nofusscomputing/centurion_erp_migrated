from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework import generics, viewsets

from access.mixin import OrganizationMixin

from api.serializers.core.ticket import TicketSerializer
from api.views.mixin import OrganizationPermissionAPI

from core.models.ticket.ticket import Ticket



class View(OrganizationMixin, viewsets.ModelViewSet):

    permission_classes = [
        OrganizationPermissionAPI
    ]

    def get_dynamic_permissions(self):

        if self.action == 'create':

            action_keyword = 'add'

        elif self.action == 'destroy':

            action_keyword = 'delete'

        elif self.action == 'partial_update':

            action_keyword = 'change'

        elif self.action == 'retrieve':

            action_keyword = 'view'

        else:

            raise ValueError('unable to determin the action_keyword')

        self.permission_required = [
            'core.' + action_keyword + '_ticket_' + self.kwargs['ticket_type'],
        ]

        return super().get_permission_required()


    queryset = Ticket.objects.all()

    serializer_class = TicketSerializer


    # def get_object(self, queryset=None, **kwargs):
    #     item = self.kwargs.get('pk')
    #     return get_object_or_404(Ticket, pk=item)


    @extend_schema(
        summary='Create a ticket',
        description = """This model includes all of the ticket comment types. 
        Due to this not all fields will be available and what fields are available
        depends upon the comment type. see
        [administration docs](https://nofusscomputing.com/projects/centurion_erp/administration/core/ticketing/index.html) for more info.
        """,
        request = TicketSerializer,
        responses = {
            201: OpenApiResponse(description='Ticket created', response=TicketSerializer),
            403: OpenApiResponse(description='User tried to edit field they dont have access to'),
        }
    )
    def create(self, request, *args, **kwargs):

        return super().create(request, *args, **kwargs)


    @extend_schema(
        summary='Fetch all tickets',
        description = """This model includes all of the ticket comment types. 
        Due to this not all fields will be available and what fields are available
        depends upon the comment type. see
        [administration docs](https://nofusscomputing.com/projects/centurion_erp/administration/core/ticketing/index.html) for more info.
        """,
        methods=["GET"],
        responses = {
            200: OpenApiResponse(description='Success', response=TicketSerializer),
        }
    )
    def list(self, request, *args, **kwargs):

        return super().list(request, *args, **kwargs)


    @extend_schema(
        summary='Fetch the selected ticket',
        description = """This model includes all of the ticket comment types. 
        Due to this not all fields will be available and what fields are available
        depends upon the comment type. see
        [administration docs](https://nofusscomputing.com/projects/centurion_erp/administration/core/ticketing/index.html) for more info.
        """,
        methods=["GET"]
    )
    def retrieve(self, request, *args, **kwargs):

        return super().retrieve(request, *args, **kwargs)


    def get_queryset(self):

        if self.kwargs['ticket_type'] == 'change':

            ticket_type = self.queryset.model.TicketType.CHANGE.value

        elif self.kwargs['ticket_type'] == 'incident':

            ticket_type = self.queryset.model.TicketType.INCIDENT.value

        elif self.kwargs['ticket_type'] == 'problem':

            ticket_type = self.queryset.model.TicketType.PROBLEM.value

        elif self.kwargs['ticket_type'] == 'request':

            ticket_type = self.queryset.model.TicketType.REQUEST.value

        else:

            raise ValueError('Unknown ticket type. kwarg `ticket_type` must be set')

        return self.queryset.filter(
            ticket_type = ticket_type
        )


    def get_view_name(self):


        # if self.kwargs['ticket_type'] == 'change':

        #     ticket_type = 'Request'

        # elif self.kwargs['ticket_type'] == 'incident':

        #     ticket_type = 'Incident'

        # elif self.kwargs['ticket_type'] == 'problem':

        #     ticket_type = 'Problem'

        # elif self.kwargs['ticket_type'] == 'request':

        #     ticket_type = 'Request'


        # if self.detail:
        #     return ticket_type + " Ticket"
        
        # return ticket_type + ' Tickets'

        if self.detail:
            return "Ticket"
        
        return 'Tickets'
