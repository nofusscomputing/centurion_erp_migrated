from django.utils.safestring import mark_safe

from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse



class Index(views.APIView):

    permission_classes = [
        IsAuthenticated,
    ]


    def get_view_name(self):
        return "ITIM"

    def get_view_description(self, html=False) -> str:
        text = "ITIM Module"
        if html:
            return mark_safe(f"<p>{text}</p>")
        else:
            return text


    def get(self, request, *args, **kwargs):

        body: dict = {
            'changes': reverse('API:_api_itim_change-list', request=request, kwargs={'ticket_type': 'change'}),
            'incidents': reverse('API:_api_itim_incident-list', request=request, kwargs={'ticket_type': 'incident'}),
            'problems': reverse('API:_api_itim_problem-list', request=request, kwargs={'ticket_type': 'problem'}),
        }

        return Response(body)
