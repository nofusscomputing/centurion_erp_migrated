from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from api.viewsets.common import ModelViewSet

from itim.serializers.service import (
    Service,
    ServiceModelSerializer,
    ServiceViewSerializer
)



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a service',
        description="""Add a new device to the ITAM database.
        If you attempt to create a device and a device with a matching name and uuid or name and serial number
        is found within the database, it will not re-create it. The device will be returned within the message body.
        """,
        responses = {
            201: OpenApiResponse(description='Device created', response=ServiceViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a service',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all services',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ServiceViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single service',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ServiceViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a service',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=ServiceViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):

    filterset_fields = [
        'name',
        'cluster',
        'device',
        'port',
    ]

    search_fields = [
        'name',
    ]

    model = Service

    view_description = 'Physical Devices'

    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()[str( self.model._meta.verbose_name) + 'ViewSerializer']


        return globals()[str( self.model._meta.verbose_name) + 'ModelSerializer']
