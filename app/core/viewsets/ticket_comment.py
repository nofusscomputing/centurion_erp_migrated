from django.db.models import Q
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, PolymorphicProxySerializer

from rest_framework import generics, viewsets
from rest_framework.response import Response

from access.mixin import OrganizationMixin

from api.views.mixin import OrganizationPermissionAPI
from api.viewsets.common import ModelViewSet

from core.serializers.ticket_comment import (
    Ticket,
    TicketComment,
    TicketCommentImportModelSerializer,
    TicketCommentITILFollowUpModelSerializer,
    TicketCommentITILSolutionModelSerializer,
    TicketCommentITILTaskModelSerializer,
    TicketCommentModelSerializer,
    TicketCommentViewSerializer
)

from settings.models.user_settings import UserSettings



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a ticket comment',
        description="""Ticket Comment API requests depend upon the users permission and comment type. 
        To view an examaple of a request, select the correct schema _Link above example, called schema_.

Responses from the API are the same for all users when the request returns 
        status `HTTP/20x`.
        """,
        request = PolymorphicProxySerializer(
            component_name = 'TicketComment',
            serializers=[
                TicketCommentImportModelSerializer,
                TicketCommentITILFollowUpModelSerializer,
                TicketCommentITILSolutionModelSerializer,
                TicketCommentITILTaskModelSerializer,
                TicketCommentModelSerializer
            ],
            resource_type_field_name=None,
            many = False
        ),
        responses = {
            201: OpenApiResponse(description='Created', response=TicketCommentViewSerializer),
            403: OpenApiResponse(description='User is missing add permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a ticket comment',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all ticket comments',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=TicketCommentViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single ticket comment',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=TicketCommentViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a ticket comment',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=TicketCommentViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet(ModelViewSet):

    filterset_fields = [
        'category',
        'external_system',
        'organization',
    ]

    search_fields = [
        'body',
    ]

    model = TicketComment


    def get_queryset(self):

        queryset = super().get_queryset()

        if 'parent_id' in self.kwargs:

            queryset = queryset.filter(parent=self.kwargs['parent_id'])

        else:

            queryset = queryset.filter(parent=None)


        if 'ticket_id' in self.kwargs:

            queryset = queryset.filter(ticket=self.kwargs['ticket_id'])

        if 'pk' in self.kwargs:

            queryset = queryset.filter(pk = self.kwargs['pk'])

        self.queryset = queryset

        return self.queryset


    def get_serializer_class(self):

        organization:int = None

        serializer_prefix:str = 'TicketComment'

        if (
            self.action == 'create'
        ):

            ticket = Ticket.objects.get(pk = int(self.kwargs['ticket_id']))

            organization = int(ticket.organization.id)

            if organization:

                if self.has_organization_permission(
                    organization = organization,
                    permissions_required = [
                        'core.import_ticketcomment'
                    ]
                ):

                    serializer_prefix = serializer_prefix + 'Import'

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()[str(serializer_prefix).replace(' ', '') + 'ViewSerializer']


        return globals()[str(serializer_prefix).replace(' ', '') + 'ModelSerializer']



    def get_view_name(self):

        if hasattr(self, 'kwargs'):

            if 'parent_id' in self.kwargs:

                if self.detail:
                    return "Ticket Comment Thread"
                
                return 'Ticket Comment Threads'

        if self.detail:
            return "Ticket Comment"
        
        return 'Ticket Comments'
