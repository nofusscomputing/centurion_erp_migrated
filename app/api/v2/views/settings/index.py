from django.utils.safestring import mark_safe

from rest_framework import generics, permissions, routers, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.v2.views.metadata import NavigationMetadata


class Index(viewsets.ViewSet):

    metadata_class = NavigationMetadata

    permission_classes = []

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
                "device_model": reverse('API:_api_v2_device_model-list', request=request),
                "external_link": reverse('API:_api_v2_external_link-list', request=request)
            }
        )
