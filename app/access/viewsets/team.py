from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from access.serializers.teams import (
    Team,
    TeamModelSerializer,
    TeamViewSerializer
)

from api.viewsets.common import ModelViewSet



# @extend_schema(tags=['access'])
@extend_schema_view(
    create=extend_schema(
        summary = 'Create a team within this organization',
        description='',
        responses = {
            200: OpenApiResponse(description='Allready exists', response=TeamViewSerializer),
            201: OpenApiResponse(description='Created', response=TeamViewSerializer),
            # 400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing add permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a team from this organization',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all teams from this organization',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=TeamViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single team from this organization',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=TeamViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a team within this organization',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=TeamViewSerializer),
            # 201: OpenApiResponse(description='Created', response=OrganizationViewSerializer),
            # # 400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):

    filterset_fields = [
        'team_name',
    ]

    search_fields = [
        'team_name',
    ]

    model = Team

    documentation: str = ''

    view_description = 'Teams belonging to a single organization'

    def get_queryset(self):

        queryset = super().get_queryset()

        queryset = queryset.filter(organization_id=self.kwargs['organization_id'])

        self.queryset = queryset

        return self.queryset

    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()[str( self.model._meta.verbose_name) + 'ViewSerializer']


        return globals()[str( self.model._meta.verbose_name) + 'ModelSerializer']

