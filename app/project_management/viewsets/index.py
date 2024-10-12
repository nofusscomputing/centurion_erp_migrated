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

    view_description = "Project Management Module"

    view_name = "Project Management"


    def list(self, request, pk=None):

        return Response(
            {
                "project": "ToDo",
            }
        )
