from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from api.viewsets.common import ModelViewSet

from project_management.serializers.project import (
    Project,
    ProjectImportSerializer,
    ProjectModelSerializer,
    ProjectViewSerializer,
    Organization,
)

from settings.models.user_settings import UserSettings



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a cluster',
        description='',
        responses = {
            201: OpenApiResponse(description='Device created', response=ProjectViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a cluster',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all clusters',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ProjectViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single cluster',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ProjectViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a cluster',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=ProjectViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):

    filterset_fields = [
        'organization',
        'external_system',
        'priority',
        'project_type',
        'state',
    ]

    search_fields = [
        'name',
        'description',
    ]

    model = Project

    view_description = 'Physical Devices'


    def get_serializer_class(self):

        organization = None

        if 'organization' in self.request.data:

            organization = int(self.request.data['organization'])

            organization = Organization.objects.get( pk = organization )

        elif self.queryset:
        
            if list(self.queryset) == 1:

                obj = list(self.queryset)[0]

                organization = obj.organization


        if organization:

            if self.request.tenancy.has_organization_permission(
                organization = organization,
                permissions_required = 'project_management.import_project'
            ) or self.request.user.is_superuser:

                return globals()[str( self.model._meta.verbose_name) + 'ImportSerializer']


        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()[str( self.model._meta.verbose_name) + 'ViewSerializer']


        return globals()[str( self.model._meta.verbose_name) + 'ModelSerializer']
