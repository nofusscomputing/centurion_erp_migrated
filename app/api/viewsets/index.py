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

    view_description = """Centurion ERP API V2.

    This endpoint will move to path `/api/` on release of 
    v2.0.0 of Centurion ERP.
    """

    view_name = "API v2"


    def list(self, request, *args, **kwargs):

        return Response(
            {
                "access": reverse('API:_api_v2_access_home-list', request=request),
                "assistance": reverse('API:_api_v2_assistance_home-list', request=request),
                "itam": reverse('API:_api_v2_itam_home-list', request=request),
                "itim": reverse('API:_api_v2_itim_home-list', request=request),
                "config_management": reverse('API:_api_v2_config_management_home-list', request=request),
                "settings": reverse('API:_api_v2_settings_home-list', request=request)
            }
        )
