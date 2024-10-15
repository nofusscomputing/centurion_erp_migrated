from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from api.viewsets.common import ReadOnlyModelViewSet

from app.serializers.permission import (
    Permission,
    PermissionViewSerializer
)



@extend_schema_view(
    list = extend_schema(
        summary = 'Fetch all permissions',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=PermissionViewSerializer),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a permission',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=PermissionViewSerializer),
        }
    ),
)
class ViewSet(
    ReadOnlyModelViewSet
):


    documentation: str = ''

    model = Permission

    view_description = 'Centurion Permissions'


    def get_serializer_class(self):

        return PermissionViewSerializer

    def get_view_name(self):

        if self.detail:

            return 'Permission'
        
        return 'Permissions'
