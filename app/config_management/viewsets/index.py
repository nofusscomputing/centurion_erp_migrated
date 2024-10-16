from drf_spectacular.utils import extend_schema

from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.viewsets.common import CommonViewSet



@extend_schema(exclude = True)
class Index(CommonViewSet):

    allowed_methods: list = [
        'GET',
        'HEAD',
        'OPTIONS'
    ]

    view_description = "Configuration Management Module"

    view_name = "Configuration Management"


    def list(self, request, pk=None):

        return Response(
            {
                "group": reverse('API:_api_v2_config_group-list', request=request),
            }
        )
