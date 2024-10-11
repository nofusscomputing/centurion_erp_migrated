from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework import generics, viewsets

from access.mixin import OrganizationMixin

from api.serializers.core.ticket_comment_category import TicketCommentCategory, TicketCommentCategorySerializer
from api.views.mixin import OrganizationPermissionAPI



class View(OrganizationMixin, viewsets.ModelViewSet):

    permission_classes = [
        OrganizationPermissionAPI
    ]

    queryset = TicketCommentCategory.objects.all()

    serializer_class = TicketCommentCategorySerializer


    @extend_schema(
        summary='Create a ticket comment category',
        request = TicketCommentCategorySerializer,
        responses = {
            201: OpenApiResponse(description='Ticket category created', response=TicketCommentCategorySerializer),
            403: OpenApiResponse(description='User tried to edit field they dont have access to'),
        }
    )
    def create(self, request, *args, **kwargs):

        return super().create(request, *args, **kwargs)


    @extend_schema(
        summary='Fetch all of the ticket comment categories',
        methods=["GET"],
        responses = {
            200: OpenApiResponse(description='Success', response=TicketCommentCategorySerializer),
        }
    )
    def list(self, request, *args, **kwargs):

        return super().list(request, *args, **kwargs)


    @extend_schema(
        summary='Fetch the selected ticket comment category',
        methods=["GET"],
        responses = {
            200: OpenApiResponse(description='Success', response=TicketCommentCategorySerializer),
        }
    )
    def retrieve(self, request, *args, **kwargs):

        return super().retrieve(request, *args, **kwargs)


    @extend_schema(
        summary='Update a ticket comment category',
        methods=["PUT"],
        responses = {
            200: OpenApiResponse(description='Ticket comment updated', response=TicketCommentCategorySerializer),
            403: OpenApiResponse(description='User tried to edit field they dont have access to'),
        }
    )
    def update(self, request, *args, **kwargs):

        return super().update(request, *args, **kwargs)


    def get_view_name(self):
        if self.detail:
            return "Ticket Comment Category"
        
        return 'Ticket Comment Categories'
