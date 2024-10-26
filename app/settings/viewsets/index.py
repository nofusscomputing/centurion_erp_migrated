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
            "name": "Application",
            "links": [
                {
                    "name": "Settings",
                    "model": "app_settings"
                }
            ]
        },
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
            "name": "Common",
            "links": [
                {
                    "name": "Manufacturers",
                    "model": "manufacturer"
                }
            ]
        },
        {
            "name": "Core",
            "links": [
                {
                    "name": "External Links",
                    "model": "external_link"
                },
                {
                    "name": "Ticket Category",
                    "model": "ticket_category"
                }
            ]
        },
        {
            "name": "ITAM",
            "links": [
                {
                    "name": "Device Model",
                    "model": "device_model"
                },
                {
                    "name": "Device Type",
                    "model": "device_type"
                },
                {
                    "name": "Software Category",
                    "model": "software_category"
                }
            ]
        },
        {
            "name": "ITIM",
            "links": [
                {
                    "name": "Cluster Type",
                    "model": "cluster_type"
                },
                {
                    "name": "Service Port",
                    "model": "port"
                },
            ]
        },
        {
            "name": "Project Management",
            "links": [
                {
                    "name": "Project State",
                    "model": "project_state"
                },
                {
                    "name": "Project Type",
                    "model": "project_type"
                },
            ]
        }
    ]

    view_description = "Centurion ERP Settings"

    view_name = "Settings"


    def list(self, request, pk=None):

        return Response(
            {
                "app_settings": reverse('v2:_api_v2_app_settings-detail', request=request, kwargs={'pk': 1}),
                "celery_log": reverse('v2:_api_v2_celery_log-list', request=request),
                "cluster_type": reverse('v2:_api_v2_cluster_type-list', request=request),
                "device_model": reverse('v2:_api_v2_device_model-list', request=request),
                "device_type": reverse('v2:_api_v2_device_type-list', request=request),
                "external_link": reverse('v2:_api_v2_external_link-list', request=request),
                "knowledge_base_category": reverse('v2:_api_v2_knowledge_base_category-list', request=request),
                "manufacturer": reverse('v2:_api_v2_manufacturer-list', request=request),
                "port": reverse('v2:_api_v2_port-list', request=request),
                "project_state": reverse('v2:_api_v2_project_state-list', request=request),
                "project_type": reverse('v2:_api_v2_project_type-list', request=request),
                "software_category": reverse('v2:_api_v2_software_category-list', request=request),
                "ticket_category": reverse('v2:_api_v2_ticket_category-list', request=request),
                "user_settings": reverse(
                    'v2:_api_v2_user_settings-detail',
                    request=request,
                    kwargs={
                        'pk': request.user.id 
                    }
                ),
            }
        )
