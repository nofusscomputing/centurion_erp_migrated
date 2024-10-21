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

    view_description = "Information Technology Infrastructure Management (ITIM) Module"

    view_name = "ITIM"


    def list(self, request, pk=None):

        return Response(
            {
                "change": "ToDo",
                "cluster": reverse('API:_api_v2_cluster-list', request=request),
                "incident": "ToDo",
                "problem": "ToDo",
                "service": reverse('API:_api_v2_service-list', request=request),
            }
        )
