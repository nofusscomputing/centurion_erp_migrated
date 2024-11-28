from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from api.viewsets.common import ModelViewSet

from config_management.serializers.config_group_software import (
    ConfigGroupSoftware,
    ConfigGroupSoftwareModelSerializer,
    ConfigGroupSoftwareViewSerializer
)



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a config group software',
        description='',
        responses = {
            # 200: OpenApiResponse(description='Allready exists', response=ConfigGroupSoftwareViewSerializer),
            201: OpenApiResponse(description='Created', response=ConfigGroupSoftwareViewSerializer),
            # 400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing add permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a config group software',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all config group softwares',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ConfigGroupSoftwareViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single config group software',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ConfigGroupSoftwareViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a config group software',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=ConfigGroupSoftwareViewSerializer),
            # 201: OpenApiResponse(description='Created', response=OrganizationViewSerializer),
            # # 400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):

    filterset_fields = [
        'organization',
        'software',
        'is_global',
    ]


    model = ConfigGroupSoftware

    documentation: str = ''

    view_description = 'Software for a config group'


    def get_queryset(self):

        if 'config_group_id' in self.kwargs:

            self.queryset = super().get_queryset().filter(config_group = self.kwargs['config_group_id'])

        else:

            self.queryset = super().get_queryset()
        
        return self.queryset


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ViewSerializer']


        return globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ModelSerializer']

