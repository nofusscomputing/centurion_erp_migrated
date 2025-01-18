from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse

from itam.serializers.operating_system_version import (
    OperatingSystem,
    OperatingSystemVersion,
    OperatingSystemVersionModelSerializer,
    OperatingSystemVersionViewSerializer
)
from api.viewsets.common import ModelViewSet



@extend_schema_view(
    create=extend_schema(
        summary = 'Create an operating system version',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'operating_system_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='Software allready exists', response=OperatingSystemVersionViewSerializer),
            201: OpenApiResponse(description='Software created', response=OperatingSystemVersionViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete an operating system version',
        description = '',
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'operating_system_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all operating system versions',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'operating_system_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response=OperatingSystemVersionViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single operating system version',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'operating_system_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response=OperatingSystemVersionViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update an operating system version',
        description = '',
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'operating_system_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response=OperatingSystemVersionViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):
    """ Operating Systems """

    filterset_fields = [
        'is_global',
        'organization',
    ]

    search_fields = [
        'name',
    ]

    model = OperatingSystemVersion

    parent_model = OperatingSystem

    parent_model_pk_kwarg = 'operating_system_id'

    view_description = 'Operating Systems'


    def get_queryset(self):

        queryset = super().get_queryset()

        queryset = queryset.filter(
            operating_system_id = self.kwargs['operating_system_id']
        )

        self.queryset = queryset

        return self.queryset


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()[str( self.model._meta.verbose_name).replace(' ' , '') + 'ViewSerializer']


        return globals()[str( self.model._meta.verbose_name).replace(' ' , '') + 'ModelSerializer']
