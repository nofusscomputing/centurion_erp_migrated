from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
    PolymorphicProxySerializer,
)

from itim.serializers.change import (
    ChangeAddTicketModelSerializer,
    ChangeChangeTicketModelSerializer,
    ChangeImportTicketModelSerializer,
    ChangeTriageTicketModelSerializer,
    ChangeTicketViewSerializer,
)

from core.viewsets.ticket import TicketViewSet



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a Change Ticket',
        description='',
        request = PolymorphicProxySerializer(
            component_name = 'ChangeTicket',
            serializers=[
                ChangeImportTicketModelSerializer,
                ChangeAddTicketModelSerializer,
                ChangeChangeTicketModelSerializer,
                ChangeTriageTicketModelSerializer,
            ],
            resource_type_field_name=None,
            many = False
        ),
        responses = {
            201: OpenApiResponse(description='Created', response=ChangeTicketViewSerializer),
            403: OpenApiResponse(description='User is missing add permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a Change Ticket',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all Change Tickets',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ChangeTicketViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a Change Ticket',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ChangeTicketViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a Change Ticket',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=ChangeTicketViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet(TicketViewSet):
    """Change Ticket

    This class exists only for the purpose of swagger for documentation.

    Args:
        TicketViewSet (class): Base Ticket ViewSet.
    """

    _ticket_type: str = 'Change'
