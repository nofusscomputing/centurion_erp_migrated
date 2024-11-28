from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse,
    PolymorphicProxySerializer,
)

from project_management.serializers.project_task import (
    ProjectTaskAddTicketModelSerializer,
    ProjectTaskChangeTicketModelSerializer,
    ProjectTaskImportTicketModelSerializer,
    ProjectTaskTriageTicketModelSerializer,
    ProjectTaskTicketViewSerializer,
)

from core.viewsets.ticket import TicketViewSet



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a Project Task',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'project_id',
                location = 'path',
                type = int
            ),
        ],
        request = PolymorphicProxySerializer(
            component_name = 'ProjectTask',
            serializers=[
                ProjectTaskImportTicketModelSerializer,
                ProjectTaskAddTicketModelSerializer,
                ProjectTaskChangeTicketModelSerializer,
                ProjectTaskTriageTicketModelSerializer,
            ],
            resource_type_field_name=None,
            many = False
        ),
        responses = {
            201: OpenApiResponse(description='Created', response=ProjectTaskTicketViewSerializer),
            403: OpenApiResponse(description='User is missing add permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a Project Task',
        description = '',
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'project_id',
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
        summary = 'Fetch all Project Task',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'project_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response=ProjectTaskTicketViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a Project Task',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'project_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response=ProjectTaskTicketViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a Project Task',
        description = '',
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'project_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response=ProjectTaskTicketViewSerializer),
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

    _ticket_type: str = 'Project Task'
