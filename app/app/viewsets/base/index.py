from drf_spectacular.utils import extend_schema

from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.viewsets.common import CommonViewSet



@extend_schema(exclude = True)
class Index(CommonViewSet):

    allowed_methods: list = [
        'GET',
        'OPTIONS'
    ]

    view_description = "Base Objects"

    view_name = "Base"


    def list(self, request, pk=None):

        return Response(
            {
                "content_type": reverse('API:_api_v2_content_type-list', request=request),
                "permission": reverse('API:_api_v2_permission-list', request=request),
                "user": reverse('API:_api_v2_user-list', request=request)
            }
        )
