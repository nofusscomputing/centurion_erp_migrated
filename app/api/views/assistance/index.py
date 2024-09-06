from django.utils.safestring import mark_safe

from rest_framework import generics, permissions, routers, views
# from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse



class Index(views.APIView):

    permission_classes = [
        IsAuthenticated,
    ]


    def get_view_name(self):
        return "Assistance"

    def get_view_description(self, html=False) -> str:
        text = "Assistance Module"
        if html:
            return mark_safe(f"<p>{text}</p>")
        else:
            return text


    def get(self, request, *args, **kwargs):

        body: dict = {
            'requests': reverse('API:_api_assistance_request-list', request=request)
        }

        return Response(body)
