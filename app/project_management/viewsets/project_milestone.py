from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse

from api.viewsets.common import ModelViewSet

from project_management.serializers.project_milestone import (
    ProjectMilestone,
    ProjectMilestoneModelSerializer,
    ProjectMilestoneViewSerializer
)



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a cluster',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'project_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            201: OpenApiResponse(description='Device created', response=ProjectMilestoneViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a cluster',
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
        summary = 'Fetch all clusters',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'project_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response=ProjectMilestoneViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single cluster',
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
            200: OpenApiResponse(description='', response=ProjectMilestoneViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a cluster',
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
            200: OpenApiResponse(description='', response=ProjectMilestoneViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):

    filterset_fields = []

    search_fields = [
        'name',
        'description',
    ]

    model = ProjectMilestone

    documentation: str = 'https://nofusscomputing.com/docs/not_model_docs'

    view_description = 'Physical Devices'


    def get_queryset(self):

        queryset = super().get_queryset()

        queryset = queryset.filter( project_id = self.kwargs['project_id'])

        self.queryset = queryset

        return self.queryset


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ViewSerializer']


        return globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ModelSerializer']
