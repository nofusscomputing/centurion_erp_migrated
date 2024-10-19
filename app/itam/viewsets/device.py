from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from api.viewsets.common import ModelViewSet

from itam.serializers.device import (
    Device,
    DeviceModelSerializer,
    DeviceViewSerializer
)



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a device',
        description="""Add a new device to the ITAM database.
        If you attempt to create a device and a device with a matching name and uuid or name and serial number
        is found within the database, it will not re-create it. The device will be returned within the message body.
        """,
        responses = {
            200: OpenApiResponse(description='Device allready exists', response=DeviceViewSerializer),
            201: OpenApiResponse(description='Device created', response=DeviceViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a device',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all devices',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=DeviceViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single device',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=DeviceViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a device',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=DeviceViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):
    """ Device """

    filterset_fields = [
        'name',
        'serial_number',
        'organization',
        'uuid',
    ]

    search_fields = [
        'name',
        'serial_number',
        'uuid',
    ]

    model = Device

    documentation: str = 'https://nofusscomputing.com/docs/not_model_docs'

    view_description = 'Physical Devices'

    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()[str( self.model._meta.verbose_name) + 'ViewSerializer']


        return globals()[str( self.model._meta.verbose_name) + 'ModelSerializer']
