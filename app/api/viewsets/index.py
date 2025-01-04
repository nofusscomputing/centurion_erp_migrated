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

    view_description = 'Centurion ERP API V2.'

    view_name = "v2"


    def list(self, request, *args, **kwargs):

        return Response(
            {
                "access": reverse('v2:_api_v2_access_home-list', request=request),
                "assistance": reverse('v2:_api_v2_assistance_home-list', request=request),
                "docs": reverse('v2:_api_v2_docs', request=request),
                "base": reverse('v2:_api_v2_base_home-list', request=request),
                "itam": reverse('v2:_api_v2_itam_home-list', request=request),
                "itim": reverse('v2:_api_v2_itim_home-list', request=request),
                "config_management": reverse('v2:_api_v2_config_management_home-list', request=request),
                "project_management": reverse('v2:_api_v2_project_management_home-list', request=request),
                "settings": reverse('v2:_api_v2_settings_home-list', request=request)
            }
        )
