from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from api.viewsets.common import ReadOnlyModelViewSet

from app.serializers.content_type import (
    ContentType,
    ContentTypeViewSerializer
)



@extend_schema_view(
    list = extend_schema(
        summary = 'Fetch all content types',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ContentTypeViewSerializer),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a content type',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ContentTypeViewSerializer),
        }
    ),
)
class ViewSet(
    ReadOnlyModelViewSet
):


    filterset_fields = [
        'app_label',
        'model',
    ]

    documentation: str = ''

    model = ContentType

    search_fields = [
        'display_name',
    ]

    view_description = 'Centurion Content Types'


    def get_serializer_class(self):

        return ContentTypeViewSerializer

    def get_view_name(self):

        if self.detail:

            return 'Content Type'
        
        return 'Content Types'
