from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from api.viewsets.common import ModelViewSet

from itim.serializers.port import (
    Port,
    PortModelSerializer,
    PortViewSerializer
)



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a port',
        description='',
        responses = {
            201: OpenApiResponse(description='Device created', response=PortViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a port',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all ports',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=PortViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single port',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=PortViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a port',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=PortViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):

    filterset_fields = [
        'number',
        'protocol',
    ]

    search_fields = [
        'description',
    ]

    model = Port

    view_description = 'Physical Devices'

    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()[str( self.model._meta.verbose_name) + 'ViewSerializer']


        return globals()[str( self.model._meta.verbose_name) + 'ModelSerializer']
