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

    page_layout: list = [
        {
            "name": "Assistanace",
            "links": [
                {
                    "name": "Knowledge Base Categories",
                    "model": "knowledge_base_category"
                }
            ]
        },
        {
            "name": "Core",
            "links": [
                {
                    "name": "External Links",
                    "model": "external_link"
                }
            ]
        },
        {
            "name": "ITAM",
            "links": [
                {
                    "name": "Device Model",
                    "model": "device_model"
                }
            ]
        }
    ]

    view_description = "Centurion ERP Settings"

    view_name = "Settings"


    def list(self, request, pk=None):

        return Response(
            {
                "knowledge_base_category": reverse('API:_api_v2_knowledge_base_category-list', request=request),
            }
        )
