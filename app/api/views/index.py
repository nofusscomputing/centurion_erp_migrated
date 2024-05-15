from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from rest_framework import generics, permissions, routers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse



class IndexView(PermissionRequiredMixin, LoginRequiredMixin, routers.APIRootView):

    permission_required = 'access.view_organization'

    def get_view_name(self):
        return "My API"

    def get_view_description(self, html=False) -> str:
        text = "My REST API"
        if html:
            return mark_safe(f"<p>{text}</p>")
        else:
            return text


    def get(self, request, *args, **kwargs):
        return Response(
        {
            "organizations": reverse("_api_orgs", request=request),
            "teams": reverse("_api_teams", request=request),
        }
    )
