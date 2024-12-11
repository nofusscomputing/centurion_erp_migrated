from django.db.models import Q
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse, PolymorphicProxySerializer

from rest_framework import generics, viewsets
from rest_framework.response import Response

from access.mixin import OrganizationMixin

from api.views.mixin import OrganizationPermissionAPI
from api.viewsets.common import ModelViewSet

from core import exceptions as centurion_exceptions
from core.serializers.ticket_comment import (
    Ticket,
    TicketComment,
    TicketCommentImportModelSerializer,

    TicketCommentITILFollowUpAddModelSerializer,
    TicketCommentITILFollowUpChangeModelSerializer,
    TicketCommentITILFollowUpTriageModelSerializer,

    TicketCommentITILSolutionAddModelSerializer,
    TicketCommentITILSolutionChangeModelSerializer,
    TicketCommentITILSolutionTriageModelSerializer,

    TicketCommentITILTaskAddModelSerializer,
    TicketCommentITILTaskChangeModelSerializer,
    TicketCommentITILTaskTriageModelSerializer,

    TicketCommentModelSerializer,
    TicketCommentAddModelSerializer,
    TicketCommentChangeModelSerializer,
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
        parameters = [
            OpenApiParameter(
                name = 'ticket_id',
                location = 'path',
                type = int
            ),
        ],
        request = PolymorphicProxySerializer(
            component_name = 'TicketComment',
            serializers=[
                TicketCommentImportModelSerializer,

                TicketCommentITILFollowUpAddModelSerializer,
                TicketCommentITILFollowUpChangeModelSerializer,
                TicketCommentITILFollowUpTriageModelSerializer,

                TicketCommentITILSolutionAddModelSerializer,
                TicketCommentITILSolutionChangeModelSerializer,
                TicketCommentITILSolutionTriageModelSerializer,

                TicketCommentITILTaskAddModelSerializer,
                TicketCommentITILTaskChangeModelSerializer,
                TicketCommentITILTaskTriageModelSerializer,
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
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'ticket_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all ticket comments',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'ticket_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response=TicketCommentViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single ticket comment',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'ticket_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response=TicketCommentViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a ticket comment',
        description = '',
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'ticket_id',
                location = 'path',
                type = int
            ),
        ],
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
        'external_system',
        'is_template',
        'organization',
        'parent',
        'source',
        'status',
        'template',
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
            'comment_type' not in self.request.data
            and self.action == 'create'
            and self.request._request.method != 'GET'
            and self.request._request.method != 'OPTIONS'
        ):

            raise  centurion_exceptions.ValidationError(
                detail = {
                    'comment_type': 'comment type is required'
                },
                code = 'required'
            )


        ticket = Ticket.objects.get(pk = int(self.kwargs['ticket_id']))

        ticket_type = str(ticket.get_ticket_type_display()).lower().replace(' ' , '_')

        organization = int(ticket.organization.id)

        if organization:

            if self.has_organization_permission(
                organization = organization,
                permissions_required = [
                    'core.import_ticketcomment'
                ]
            ):

                if (
                    self.action == 'create'
                    or self.action == 'partial_update'
                    or self.action == 'update'
                ):
                    serializer_prefix = serializer_prefix + 'Import'

            elif (
                self.action == 'create'
                or self.action == 'partial_update'
                or self.action == 'update'
            ):

                if(
                    self.action == 'partial_update'
                    or self.action == 'update'
                ):

                    comment_type = list(self.queryset)[0].comment_type

                else:

                    if(
                        self.request._request.method != 'GET'
                    ):

                        comment_type = int(self.request.data['comment_type'])


                if(
                    self.request._request.method != 'GET'
                ):

                    if comment_type == int(TicketComment.CommentType.COMMENT):

                        serializer_prefix = serializer_prefix + 'ITILFollowUp'

                    elif comment_type == int(TicketComment.CommentType.SOLUTION):

                        serializer_prefix = serializer_prefix + 'ITILSolution'

                    elif comment_type == int(TicketComment.CommentType.TASK):

                        serializer_prefix = serializer_prefix + 'ITILTask'

                    else:

                        raise  centurion_exceptions.ValidationError(
                            detail = 'Unable to determine the serializer',
                            code = 'serializer_unknwon'
                        )


        if 'Import' not in serializer_prefix:

            if self.action == 'create':

                if self.has_organization_permission(
                    organization = ticket.organization.id,
                    permissions_required = [ 'core.triage_ticket_'+ ticket_type ],
                ) and not self.request.user.is_superuser:

                    serializer_prefix = serializer_prefix + 'Triage'

                else:

                    serializer_prefix = serializer_prefix + 'Add'


            elif (
                self.action == 'partial_update'
                or self.action == 'update'
            ):

                if self.has_organization_permission(
                    organization = ticket.organization.id,
                    permissions_required = [ 'core.triage_ticket_'+ ticket_type ],
                ) and not self.request.user.is_superuser:

                    serializer_prefix = serializer_prefix + 'Triage'

                else:

                    serializer_prefix = serializer_prefix + 'Change'


        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()['TicketCommentViewSerializer']


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
