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
        return "API Index"

    def get_view_description(self, html=False) -> str:
        text = "My REST API"
        if html:
            return mark_safe(f"<p>{text}</p>")
        else:
            return text


    def list(self, request, pk=None):

        API: dict = {
            # "teams": reverse("_api_teams", request=request),
            'assistance': reverse("API:_api_assistance", request=request),
            "devices": reverse("API:device-list", request=request),
            "config_groups": reverse("API:_api_config_groups", request=request),
            'itim': reverse("API:_api_itim", request=request),
            "organizations": reverse("API:_api_orgs", request=request),
            'project_management': reverse("API:_api_project_management", request=request),
            "settings": reverse('API:_settings', request=request),
            "software": reverse("API:software-list", request=request),

        }

        if django_settings.API_TEST:

            API.update({
                'v2': reverse("API:_api_v2_home-list", request=request),
            })

        return Response( API )
