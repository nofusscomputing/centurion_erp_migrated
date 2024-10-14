from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.react_ui_metadata import ReactUIMetadata
from api.viewsets.common import ModelViewSet

from app.serializers.user import (
    User,
    UserBaseSerializer
)



@extend_schema_view(
    list = extend_schema(
        summary = 'Fetch all users',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=UserBaseSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single user',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=UserBaseSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
)
class ViewSet(
    viewsets.ReadOnlyModelViewSet
):


    documentation: str = ''

    filterset_fields = [
        'username',
        'first_name',
        'last_name',
        'is_active'
    ]

    metadata_class = ReactUIMetadata

    model = User

    permission_classes = [
        IsAuthenticated,
    ]

    queryset = User.objects.all()

    search_fields = [
        'username',
        'first_name',
        'last_name',
    ]

    view_description = 'Centurion Users'


    def get_serializer_class(self):

        return UserBaseSerializer

    def get_view_name(self):

        if self.detail:

            return 'User'
        
        return 'Users'
