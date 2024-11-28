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
                "change": reverse('v2:_api_v2_ticket_change-list', request=request),
                "cluster": reverse('v2:_api_v2_cluster-list', request=request),
                "incident": reverse('v2:_api_v2_ticket_incident-list', request=request),
                "problem": reverse('v2:_api_v2_ticket_problem-list', request=request),
                "service": reverse('v2:_api_v2_service-list', request=request),
            }
        )
