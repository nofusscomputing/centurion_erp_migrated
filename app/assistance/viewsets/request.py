from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
    PolymorphicProxySerializer,
)

from assistance.serializers.request import (
    RequestAddTicketModelSerializer,
    RequestChangeTicketModelSerializer,
    RequestTriageTicketModelSerializer,
    RequestImportTicketModelSerializer,
    RequestTicketModelSerializer,
    RequestTicketViewSerializer
)

from core.viewsets.ticket import TicketViewSet

from settings.models.user_settings import UserSettings



@extend_schema_view(
    create = extend_schema(
        versions = [
            'v2'
        ],
        summary = 'Create a Request Ticket',
        description="""Ticket API requests depend upon the users permission. 
        To view an examaple of a request, select the correct schema _Link above example, called schema_.

Responses from the API are the same for all users when the request returns 
        status `HTTP/20x`.
        """,
        request = PolymorphicProxySerializer(
            component_name = 'Ticket',
            serializers=[
                RequestImportTicketModelSerializer,
                RequestAddTicketModelSerializer,
                RequestChangeTicketModelSerializer,
                RequestTriageTicketModelSerializer,
            ],
            resource_type_field_name=None,
            many = False
        ),
        responses = {
            201: OpenApiResponse(description='Created', response=RequestTicketViewSerializer),
            403: OpenApiResponse(description='User is missing add permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a Request Ticket',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all Request Tickets',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=RequestTicketViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a Request Ticket',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=RequestTicketViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a Request Ticket',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=RequestTicketViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet(TicketViewSet):
    """Request Ticket

    This class exists only for the purpose of swagger for documentation.

    Args:
        TicketViewSet (class): Base Ticket ViewSet.
    """

    _ticket_type: str = 'Request'
