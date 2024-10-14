from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from access.serializers.team_user import (
    TeamUsers,
    TeamUserModelSerializer,
    TeamUserViewSerializer
)

from api.viewsets.common import ModelViewSet



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a user within this team',
        description='',
        responses = {
            # 200: OpenApiResponse(description='Allready exists', response=TeamUserViewSerializer),
            201: OpenApiResponse(description='Created', response=TeamUserViewSerializer),
            # 400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing add permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a user from this team',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all users from this team',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=TeamUserViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single user from this team',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=TeamUserViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a user within this team',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=TeamUserViewSerializer),
            # 201: OpenApiResponse(description='Created', response=OrganizationViewSerializer),
            # # 400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):

    filterset_fields = [
        'manager',
        'team__organization',
    ]

    search_fields = []

    model = TeamUsers

    documentation: str = ''

    view_description = 'Users belonging to a single team'

    def get_queryset(self):

        queryset = super().get_queryset()

        queryset = queryset.filter(
            team_id = self.kwargs['team_id']
        )

        self.queryset = queryset

        return self.queryset


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ViewSerializer']


        return globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ModelSerializer']

