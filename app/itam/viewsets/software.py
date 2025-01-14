from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from itam.serializers.software import (
    Software,
    SoftwareModelSerializer,
    SoftwareViewSerializer
)
from api.viewsets.common import ModelViewSet



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a software',
        description='',
        responses = {
            200: OpenApiResponse(description='Software allready exists', response=SoftwareViewSerializer),
            201: OpenApiResponse(description='Software created', response=SoftwareViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a software',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all softwares',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=SoftwareViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single software',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=SoftwareViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a software',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=SoftwareViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):
    """ Software """

    filterset_fields = [
        'category',
        'organization',
        'publisher',
    ]

    search_fields = [
        'name',
    ]

    model = Software

    view_description = 'Physical Softwares'

    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()[str( self.model._meta.verbose_name) + 'ViewSerializer']


        return globals()[str( self.model._meta.verbose_name) + 'ModelSerializer']
