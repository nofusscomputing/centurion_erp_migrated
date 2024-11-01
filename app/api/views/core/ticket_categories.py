from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework import generics, viewsets

from access.mixin import OrganizationMixin

from api.serializers.core.ticket_category import TicketCategory, TicketCategorySerializer
from api.views.mixin import OrganizationPermissionAPI


@extend_schema(deprecated=True)
class View(OrganizationMixin, viewsets.ModelViewSet):

    permission_classes = [
        OrganizationPermissionAPI
    ]

    queryset = TicketCategory.objects.all()

    serializer_class = TicketCategorySerializer


    @extend_schema(
        summary='Create a ticket category',
        request = TicketCategorySerializer,
        responses = {
            201: OpenApiResponse(description='Ticket category created', response=TicketCategorySerializer),
            403: OpenApiResponse(description='User tried to edit field they dont have access to'),
        }
    )
    def create(self, request, *args, **kwargs):

        return super().create(request, *args, **kwargs)


    @extend_schema(
        summary='Fetch all of a tickets category',
        methods=["GET"],
        responses = {
            200: OpenApiResponse(description='Success', response=TicketCategorySerializer),
        }
    )
    def list(self, request, *args, **kwargs):

        return super().list(request, *args, **kwargs)


    @extend_schema(
        summary='Fetch the selected ticket category',
        methods=["GET"],
        responses = {
            200: OpenApiResponse(description='Success', response=TicketCategorySerializer),
        }
    )
    def retrieve(self, request, *args, **kwargs):

        return super().retrieve(request, *args, **kwargs)


    @extend_schema(
        summary='Update a ticket category',
        methods=["PUT"],
        responses = {
            200: OpenApiResponse(description='Ticket comment updated', response=TicketCategorySerializer),
            403: OpenApiResponse(description='User tried to edit field they dont have access to'),
        }
    )
    def update(self, request, *args, **kwargs):

        return super().update(request, *args, **kwargs)


    def get_view_name(self):
        if self.detail:
            return "Ticket Category"
        
        return 'Ticket Categories'
