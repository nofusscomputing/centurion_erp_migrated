from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from core.serializers.manufacturer import (
    Manufacturer,
    ManufacturerModelSerializer,
    ManufacturerViewSerializer
)

from api.viewsets.common import ModelViewSet




@extend_schema_view(
    create=extend_schema(
        summary = 'Create a manufacturer',
        description='',
        responses = {
            # 200: OpenApiResponse(description='Allready exists', response=ConfigGroupViewSerializer),
            201: OpenApiResponse(description='Created', response=ManufacturerViewSerializer),
            # 400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing add permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a manufacturer',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all manufacturer',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ManufacturerViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single manufacturer',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ManufacturerViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a manufacturer',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=ManufacturerViewSerializer),
            # 201: OpenApiResponse(description='Created', response=OrganizationViewSerializer),
            # # 400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet(ModelViewSet):

    filterset_fields = [
        'organization',
    ]

    search_fields = [
        'name',
    ]

    model = Manufacturer


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ViewSerializer']


        return globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ModelSerializer']
