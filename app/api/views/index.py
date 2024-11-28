from django.conf import settings as django_settings

from django.utils.safestring import mark_safe

from rest_framework import generics, permissions, routers, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse



class Index(viewsets.ViewSet):

    permission_classes = [
        IsAuthenticated,
    ]


    def get_view_name(self):
        return "API"

    def get_view_description(self, html=False) -> str:
        text = "Centurion ERP Rest API"
        if html:
            return mark_safe(f"<p>{text}</p>")
        else:
            return text


    def list(self, request, pk=None):

        API: dict = {
            # "teams": reverse("_api_teams", request=request),
            'assistance': reverse("v1:_api_assistance", request=request),
            "devices": reverse("v1:device-list", request=request),
            "config_groups": reverse("v1:_api_config_groups", request=request),
            'itim': reverse("v1:_api_itim", request=request),
            "organizations": reverse("v1:_api_orgs", request=request),
            'project_management': reverse("v1:_api_project_management", request=request),
            "settings": reverse('v1:_settings', request=request),
            "software": reverse("v1:software-list", request=request),
            'v2': reverse("v2:_api_v2_home-list", request=request)
        }

        return Response( API )
