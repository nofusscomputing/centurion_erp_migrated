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

    view_description = "Information Technology Asset Management (ITAM)"

    view_name = "ITAM"


    def list(self, request, pk=None):

        return Response(
            {
                "device": reverse('v2:_api_v2_device-list', request=request),
                "operating_system": reverse('v2:_api_v2_operating_system-list', request=request),
                "software": reverse('v2:_api_v2_software-list', request=request)
            }
        )
