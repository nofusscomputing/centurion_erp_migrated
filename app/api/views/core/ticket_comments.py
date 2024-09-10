from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework import generics, viewsets

from access.mixin import OrganizationMixin

from api.serializers.core.ticket_comment import TicketCommentSerializer
from api.views.mixin import OrganizationPermissionAPI

from core.models.ticket.ticket_comment import TicketComment



class View(OrganizationMixin, viewsets.ModelViewSet):

    permission_classes = [
        OrganizationPermissionAPI
    ]

    queryset = TicketComment.objects.all()

    serializer_class = TicketCommentSerializer


    @extend_schema(
        summary='Create a ticket comment',
        description = """This model includes all of the ticket comment types. 
        Due to this not all fields will be available and what fields are available
        depends upon the comment type.
        """,
        request = TicketCommentSerializer,
        responses = {
            201: OpenApiResponse(description='Ticket comment created', response=TicketCommentSerializer),
            403: OpenApiResponse(description='User tried to edit field they dont have access to'),
        }
    )
    def create(self, request, *args, **kwargs):

        return super().create(request, *args, **kwargs)


    @extend_schema(
        summary='Fetch all of a tickets comments',
        methods=["GET"],
        responses = {
            200: OpenApiResponse(description='Success', response=TicketCommentSerializer),
        }
    )
    def list(self, request, *args, **kwargs):

        return super().list(request, *args, **kwargs)


    @extend_schema(
        summary='Fetch the selected ticket Comment',
        methods=["GET"],
        responses = {
            200: OpenApiResponse(description='Success', response=TicketCommentSerializer),
        }
    )
    def retrieve(self, request, *args, **kwargs):

        return super().retrieve(request, *args, **kwargs)


    @extend_schema(
        summary='Update a ticket Comment',
        description = """This model includes all of the ticket comment types. 
        Due to this not all fields will be available and what fields are available
        depends upon the comment type.
        """,
        methods=["PUT"],
        responses = {
            200: OpenApiResponse(description='Ticket comment updated', response=TicketCommentSerializer),
            403: OpenApiResponse(description='User tried to edit field they dont have access to'),
        }
    )
    def update(self, request, *args, **kwargs):

        return super().update(request, *args, **kwargs)


    def get_queryset(self):

        if 'ticket_id' in self.kwargs:

            self.queryset = self.queryset.filter(ticket=self.kwargs['ticket_id']).order_by('created')

        if 'pk' in self.kwargs:

            self.queryset = self.queryset.filter(pk = self.kwargs['pk'])

        return self.queryset


    def get_view_name(self):
        if self.detail:
            return "Ticket Comment"
        
        return 'Ticket Comments'
