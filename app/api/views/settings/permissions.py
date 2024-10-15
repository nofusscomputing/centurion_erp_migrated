from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from access.functions import permissions

from core.http.common import Http


@extend_schema(deprecated=True)
class View(views.APIView):

    permission_classes = [
        IsAuthenticated,
    ]


    @extend_schema(
        summary = "Fetch available permissions",
        description = """This endpoint provides a list of permissions that are available within
Centurion ERP. The format of each permission is `<app name>.<permission>_<model>`.

This endpoint is available to **all** authenticated users.
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

        response_data: list = []

        try:

            for permission in permissions.permission_queryset():

                response_data += [ str(f"{permission.content_type.app_label}.{permission.codename}") ]

        except PermissionDenied as e:

            status = Http.Status.FORBIDDEN
            response_data = ''


        except Exception as e:

            print(f'An error occured{e}')

            status = Http.Status.SERVER_ERROR
            response_data = 'Unknown Server Error occured'


        return Response(data=response_data,status=status)


    def get_view_name(self):
        return "Permissions"
