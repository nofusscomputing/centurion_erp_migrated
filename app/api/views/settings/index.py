from django.contrib.auth.models import Permission

from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from core.http.common import Http



class View(views.APIView):

    permission_classes = [
        IsAuthenticated,
    ]


    @extend_schema(
        summary = "Settings Index Page",
        description = """This endpoint provides the available settings as available via the API.
        """,

        methods=["GET"],
        parameters = None,
        tags = ['settings',],
        responses = {
            200: OpenApiResponse(description='Inventory upload successful'),
            401: OpenApiResponse(description='User Not logged in'),
            500: OpenApiResponse(description='Exception occured. View server logs for the Stack Trace'),
        }
    )
    def get(self, request, *args, **kwargs):

        status = Http.Status.OK

        response_data: dict = {
            "permissions": reverse('API:_settings_permissions', request=request),
            "ticket_categories": reverse('API:_api_ticket_category-list', request=request)
        }

        return Response(data=response_data,status=status)


    def get_view_name(self):
        return "Settings"
