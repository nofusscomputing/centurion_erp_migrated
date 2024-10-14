from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from access.serializers.organization import (
    Organization,
    OrganizationModelSerializer,
    OrganizationViewSerializer
)

from api.viewsets.common import ModelViewSet



# @extend_schema(tags=['access'])
@extend_schema_view(
    create=extend_schema(
        summary = 'Create an orgnaization',
        description='',
        responses = {
            # 200: OpenApiResponse(description='Allready exists', response=OrganizationViewSerializer),
            201: OpenApiResponse(description='Created', response=OrganizationViewSerializer),
            # 400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing add permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete an orgnaization',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all orgnaizations',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=OrganizationViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single orgnaization',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=OrganizationViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update an orgnaization',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=OrganizationViewSerializer),
            # 201: OpenApiResponse(description='Created', response=OrganizationViewSerializer),
            # # 400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):

    filterset_fields = [
        'name',
        'manager',
    ]

    search_fields = [
        'name',
    ]

    model = Organization

    documentation: str = ''

    view_description = 'Centurion Organizations'

    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()[str( self.model._meta.verbose_name) + 'ViewSerializer']


        return globals()[str( self.model._meta.verbose_name) + 'ModelSerializer']

