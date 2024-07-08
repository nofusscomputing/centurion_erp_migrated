import json
import re

from django.core.exceptions import ValidationError, PermissionDenied

from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework import generics, views
from rest_framework.response import Response

from api.views.mixin import OrganizationPermissionAPI
from api.serializers.itam.inventory import InventorySerializer
from api.serializers.inventory import Inventory

from core.http.common import Http

from itam.models.device import Device

from settings.models.user_settings import UserSettings

from api.tasks import process_inventory



class InventoryPermissions(OrganizationPermissionAPI):

    def permission_check(self, request, view, obj=None) -> bool:

        data = view.request.data

        self.obj = Device.objects.get(slug=str(data.details.name).lower())

        return super().permission_check(request, view, obj=None)



class Collect(OrganizationPermissionAPI, views.APIView):

    queryset = Device.objects.all()


    @extend_schema(
        summary = "Upload a device's inventory",
        description = """After inventorying a device, it's inventory file, `.json` is uploaded to this endpoint.
If the device does not exist, it will be created. If the device does exist the existing
device will be updated with the information within the inventory.

matching for an existing device is by slug which is the hostname converted to lower case
letters. This conversion is automagic.

**NOTE:** _for device creation, the API user must have user setting 'Default Organization'. Without
this setting populated, no device will be created and the endpoint will return HTTP/403_

## Permissions

- `itam.add_device` Required to upload inventory
        """,

        methods=["POST"],
        parameters = None,
        tags = ['device', 'inventory',],
        request = InventorySerializer,
        responses = {
            200: OpenApiResponse(description='Inventory upload successful'),
            401: OpenApiResponse(description='User Not logged in'),
            403: OpenApiResponse(description='User is missing permission or in different organization'),
            500: OpenApiResponse(description='Exception occured. View server logs for the Stack Trace'),
        }
    )
    def post(self, request, *args, **kwargs):

        status = Http.Status.OK
        response_data = 'OK'

        try:

            data = json.loads(request.body)
            data = Inventory(data)

            device = None


            self.default_organization = UserSettings.objects.get(user=request.user).default_organization

            if Device.objects.filter(slug=str(data.details.name).lower()).exists():

                self.obj = Device.objects.get(slug=str(data.details.name).lower())

                device = self.obj


            if not self.permission_check(request=request, view=self, obj=device):

                raise Http404

            task = process_inventory.delay(request.body, self.default_organization.id)

            response_data: dict = {"task_id": f"{task.id}"}

        except PermissionDenied as e:

            status = Http.Status.FORBIDDEN
            response_data = ''

        except ValidationError as e:

            status = Http.Status.BAD_REQUEST
            response_data = e.message

        except Exception as e:

            print(f'An error occured{e}')

            status = Http.Status.SERVER_ERROR
            response_data = 'Unknown Server Error occured'


        return Response(data=response_data,status=status)



    def get_view_name(self):
        return "Inventory"
