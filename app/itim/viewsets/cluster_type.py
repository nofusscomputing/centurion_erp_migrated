from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from api.viewsets.common import ModelViewSet

from itim.serializers.cluster_type import (
    ClusterType,
    ClusterTypeModelSerializer,
    ClusterTypeViewSerializer
)



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a cluster type',
        description='',
        responses = {
            201: OpenApiResponse(description='Device created', response=ClusterTypeViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a cluster type',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all cluster types',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ClusterTypeViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single cluster type',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ClusterTypeViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a cluster type',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=ClusterTypeViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):

    filterset_fields = [
        'organization',
        'is_global',
    ]

    search_fields = [
        'name',
    ]

    model = ClusterType

    view_description = 'Physical Devices'


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ViewSerializer']


        return globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ModelSerializer']
