from drf_spectacular.utils import extend_schema

from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.viewsets.common import IndexViewset



@extend_schema(exclude = True)
class Index(IndexViewset):

    allowed_methods: list = [
        'GET',
        'HEAD',
        'OPTIONS'
    ]

    view_description = "Access Module"

    view_name = "Access"


    def list(self, request, pk=None):

        return Response(
            {
                "organization": reverse('v2:_api_v2_organization-list', request=request)
            }
        )
