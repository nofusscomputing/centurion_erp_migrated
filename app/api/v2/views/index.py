from django.utils.safestring import mark_safe

from rest_framework import generics, permissions, routers, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_json_api.exceptions import exception_handler
from .metadata import NavigationMetadata
from access.mixin import OrganizationMixin
from api.views.mixin import OrganizationPermissionAPI

class Index(OrganizationMixin, viewsets.ViewSet):

    metadata_class = NavigationMetadata

    permission_classes = [
        OrganizationPermissionAPI,
    ]

    def get_view_name(self):
        return "V2"

    def get_view_description(self, html=False) -> str:
        text = "Centurion ERP UI Testing"
        if html:
            return mark_safe(f"<p>{text}</p>")
        else:
            return text


    def list(self, request, pk=None):
        return Response(
            {
                "access": "to do",
                "assistance": reverse('API:_api_v2_assistance_home-list', request=request),
                "itam": reverse('API:_api_v2_itam_home-list', request=request),
                "settings": reverse('API:_api_v2_settings_home-list', request=request)
            }
        )
