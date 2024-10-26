from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from api.viewsets.common import ModelViewSet

from core.serializers.ticket_category import (
    TicketCategory,
    TicketCategoryModelSerializer,
    TicketCategoryViewSerializer
)



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a ticket category',
        description='',
        responses = {
            201: OpenApiResponse(description='Created', response=TicketCategoryViewSerializer),
            403: OpenApiResponse(description='User is missing add permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a ticket category',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all ticket categories',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=TicketCategoryViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single ticket category',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=TicketCategoryViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a ticket category',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=TicketCategoryViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet(ModelViewSet):

    filterset_fields = [
        'organization',
    ]

    search_fields = [
        'name',
    ]

    model = TicketCategory


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ViewSerializer']


        return globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ModelSerializer']
