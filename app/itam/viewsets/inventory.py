import json

from django.db.models import Q

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from rest_framework.response import Response

from api.viewsets.common import ModelCreateViewSet

from core import exceptions as centurion_exception
from core.http.common import Http

from itam.models.device import Device
from itam.serializers.inventory import InventorySerializer
from itam.tasks.inventory import process_inventory

from settings.models.user_settings import UserSettings



@extend_schema_view(
    create=extend_schema(
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
        request = InventorySerializer,
        responses = {
            200: OpenApiResponse(
                description='Inventory upload successful',
                response = {
                    'OK'
                }
            ),
            400: OpenApiResponse(description='Error Occured, see output retured'),
            401: OpenApiResponse(description='User Not logged in'),
            403: OpenApiResponse(description='User is missing permission or in different organization'),
            500: OpenApiResponse(description='Exception occured. View server logs for the Stack Trace'),
        }
    )
)
class ViewSet( ModelCreateViewSet ):
    """Device Inventory

    Use this endpoint to upload your device inventories.
    """

    model = Device

    serializer_class = InventorySerializer

    documentation: str = 'https://nofusscomputing.com/docs/not_model_docs'

    view_name = 'Device Inventory'

    view_description = __doc__

    inventory_action: str = None
    """Inventory action, choice. new|update"""


    def create(self, request, *args, **kwargs):
        """Upload a device inventory

        Raises:
            centurion_exceptions.PermissionDenied: User is missing the required permissions

        Returns:
            Response: string denoting what has occured
        """

        status = Http.Status.OK
        response_data = 'OK'

        try:

            data = InventorySerializer(
                data = request.data
            )

            device = None

            if not data.is_valid():

                raise centurion_exception.ValidationError(
                    detail = 'Uploaded inventory is not valid',
                    code = 'invalid_inventory'
                )


            self.default_organization = UserSettings.objects.get(user=request.user).default_organization

            obj_organaization_id = getattr(self.default_organization, 'id', None)


            obj = Device.objects.filter(
                Q(
                    name=str(data.validated_data['details']['name']).lower(),
                    serial_number = str(data.validated_data['details']['serial_number']).lower()

                )
                  |
                Q(
                    name = str(data.validated_data['details']['name']).lower(),
                    uuid = str(data.validated_data['details']['uuid']).lower()
                )
            )


            if len(obj) == 1:

                obj_organaization_id = obj[0].organization.id


            if not obj_organaization_id:

                raise centurion_exception.ValidationError({
                    'detail': 'No Default organization set for user'
                })

            task = process_inventory.delay(data.validated_data, obj_organaization_id)

            response_data: dict = {"task_id": f"{task.id}"}


        except centurion_exception.PermissionDenied as e:

            status = Http.Status.FORBIDDEN
            response_data = e.detail

        except centurion_exception.ValidationError as e:

            status = Http.Status.BAD_REQUEST
            response_data = e.detail

        except Exception as e:

            print(f'An error occured{e}')

            status = Http.Status.SERVER_ERROR
            response_data = f'Unknown Server Error occured: {e}'


        return Response(data=response_data,status=status)



    def get_dynamic_permissions(self):
        """Obtain the permissions required to upload an inventory.

        Returns:
            list: Permissions required for Inventory Upload
        """

        organization = None

        device_search = None

        if 'details' in self.request.data:

            if 'name' in self.request.data['details']:

                device_search = Device.objects.filter(
                    slug = str(self.request.data['details']['name']).lower()
                )

            else:

                centurion_exception.ParseError(
                    detail = {
                        'name': 'Device name is required'
                    },
                    code = 'missing_device_name'
                )

        else:

            centurion_exception.ParseError(
                detail = {
                    'details': 'Details dict is required'
                },
                code = 'missing_details_dict'
            )


        if device_search:    # Existing device

            if len(list(device_search)) == 1:

                self.obj = list(device_search)[0]

            self.permission_required = [
                'itam.change_device'
            ]

            self.inventory_action = 'update'

        else:    # New device

            self.permission_required = [
                'itam.add_device'
            ]

            self.inventory_action = 'new'


        return super().get_permission_required()


    def get_serializer_class(self):
        return InventorySerializer
