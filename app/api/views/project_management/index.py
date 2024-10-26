from django.utils.safestring import mark_safe

from drf_spectacular.utils import extend_schema

from rest_framework import generics, permissions, routers, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse


@extend_schema(deprecated=True)
class Index(views.APIView):

    permission_classes = [
        IsAuthenticated,
    ]


    def get_view_name(self):
        return "Projects"

    def get_view_description(self, html=False) -> str:
        text = "Projects Managementn Module"
        if html:
            return mark_safe(f"<p>{text}</p>")
        else:
            return text


    def get(self, request, *args, **kwargs):

        body: dict = {
            'projects': reverse('v1:_api_projects-list', request=request)
        }

        return Response(body)
