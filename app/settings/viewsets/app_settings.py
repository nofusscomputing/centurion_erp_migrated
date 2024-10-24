from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from api.viewsets.common import ModelViewSet

from settings.serializers.app_settings import (
    AppSettings,
    AppSettingsModelSerializer,
    AppSettingsViewSerializer
)



@extend_schema_view(
    create=extend_schema(
        summary = 'Create an app setting',
        description="""Add a new device to the ITAM database.
        If you attempt to create a device and a device with a matching name and uuid or name and serial number
        is found within the database, it will not re-create it. The device will be returned within the message body.
        """,
        responses = {
            201: OpenApiResponse(description='Device created', response=AppSettingsViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete an app setting',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all app settings',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=AppSettingsViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch app settings',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=AppSettingsViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update an app setting',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=AppSettingsViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet(ModelViewSet):

    model = AppSettings

    # filterset_fields = [
    #     'cluster',
    #     'devices',
    #     'software',
    # ]


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ViewSerializer']


        return globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ModelSerializer']
