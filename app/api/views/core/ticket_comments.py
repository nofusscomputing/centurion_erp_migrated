from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema

from rest_framework import generics, viewsets

from access.mixin import OrganizationMixin

from api.serializers.itim.ticket_comment import TicketCommentSerializer
from api.views.mixin import OrganizationPermissionAPI

from core.models.ticket.ticket_comment import TicketComment



class View(OrganizationMixin, viewsets.ModelViewSet):

    permission_classes = [
        OrganizationPermissionAPI
    ]

    queryset = TicketComment.objects.all()

    serializer_class = TicketCommentSerializer


    @extend_schema( description='Fetch all tickets', methods=["GET"])
    def list(self, request, ticket_id):

        return super().list(request)


    @extend_schema( description='Fetch the selected ticket', methods=["GET"])
    def retrieve(self, request, *args, **kwargs):

        return super().retrieve(request, *args, **kwargs)


    def get_queryset(self):

        if 'pk' in self.kwargs:

            self.queryset = self.queryset.filter(pk = self.kwargs['pk'])

        return self.queryset


    def get_view_name(self):
        if self.detail:
            return "Ticket Comment"
        
        return 'Ticket Comments'
