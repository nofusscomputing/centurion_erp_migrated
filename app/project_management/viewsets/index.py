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

    view_description = "Project Management Module"

    view_name = "Project Management"


    def list(self, request, pk=None):

        return Response(
            {
                "project": reverse('v2:_api_v2_project-list', request=request),
            }
        )
