from django.db.models import Q

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse

from access.mixin import OrganizationMixin

from api.viewsets.common import ModelListRetrieveDeleteViewSet

from core.serializers.ticket_related import (
    RelatedTickets,
    RelatedTicketModelSerializer,
    RelatedTicketViewSerializer,
)



@extend_schema_view(
    destroy = extend_schema(
        summary = 'Delete a related ticket',
        description = '',
        parameters = [
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
        summary = 'Fetch all related tickets',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'ticket_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response=RelatedTicketViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a related ticket',
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
            200: OpenApiResponse(description='', response=RelatedTicketViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
)
class ViewSet(ModelListRetrieveDeleteViewSet):


    filterset_fields = [
        'organization',
    ]

    search_fields = [
        'name',
    ]

    model = RelatedTickets


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ViewSerializer']


        return globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ModelSerializer']


    def get_queryset(self):

        self.queryset = RelatedTickets.objects.filter(
            Q(from_ticket_id_id=self.kwargs['ticket_id'])
                |
            Q(to_ticket_id_id=self.kwargs['ticket_id'])
        )

        return self.queryset.filter().order_by('id')
