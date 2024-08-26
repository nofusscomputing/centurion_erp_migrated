from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema

from rest_framework import generics, viewsets

from access.mixin import OrganizationMixin

from api.serializers.itim.ticket import TicketSerializer
from api.views.mixin import OrganizationPermissionAPI

from core.models.ticket.ticket import Ticket



class View(OrganizationMixin, viewsets.ModelViewSet):

    permission_classes = [
        OrganizationPermissionAPI
    ]

    queryset = Ticket.objects.all()

    serializer_class = TicketSerializer


    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(Ticket, pk=item)


    @extend_schema( description='Fetch all tickets', methods=["GET"])
    def list(self, request):

        return super().list(request)


    @extend_schema( description='Fetch the selected ticket', methods=["GET"])
    def retrieve(self, request, *args, **kwargs):

        return super().retrieve(request, *args, **kwargs)


    def get_queryset(self):

        return self.queryset


    def get_view_name(self):
        if self.detail:
            return "Ticket"
        
        return 'Tickets'
