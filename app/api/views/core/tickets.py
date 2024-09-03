from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework import generics, viewsets

from access.mixin import OrganizationMixin

from api.serializers.itim.ticket import TicketSerializer
from api.views.mixin import OrganizationPermissionAPI

from core.models.ticket.ticket import Ticket



class View(OrganizationMixin, viewsets.ModelViewSet):

    permission_classes = [
        OrganizationPermissionAPI
    ]

    def get_dynamic_permissions(self):

        self.permission_required = [
            'core.view_ticket_request',
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

        super().create(request, *args, **kwargs)


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
    def list(self, request):

        return super().list(request)


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

        return self.queryset


    def get_view_name(self):
        if self.detail:
            return "Ticket"
        
        return 'Tickets'
