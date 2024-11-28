from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
    PolymorphicProxySerializer,
)

from itim.serializers.incident import (
    IncidentAddTicketModelSerializer,
    IncidentChangeTicketModelSerializer,
    IncidentImportTicketModelSerializer,
    IncidentTriageTicketModelSerializer,
    IncidentTicketViewSerializer,
)

from core.viewsets.ticket import TicketViewSet



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a Incident Ticket',
        description='',
        request = PolymorphicProxySerializer(
            component_name = 'IncidentTicket',
            serializers=[
                IncidentImportTicketModelSerializer,
                IncidentAddTicketModelSerializer,
                IncidentChangeTicketModelSerializer,
                IncidentTriageTicketModelSerializer,
            ],
            resource_type_field_name=None,
            many = False
        ),
        responses = {
            201: OpenApiResponse(description='Created', response=IncidentTicketViewSerializer),
            403: OpenApiResponse(description='User is missing add permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a Incident Ticket',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all Incident Tickets',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=IncidentTicketViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a Incident Ticket',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=IncidentTicketViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a Incident Ticket',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=IncidentTicketViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet(TicketViewSet):
    """Incident Ticket

    This class exists only for the purpose of swagger for documentation.

    Args:
        TicketViewSet (class): Base Ticket ViewSet.
    """

    _ticket_type: str = 'Incident'
