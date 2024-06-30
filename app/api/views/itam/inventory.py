# from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
import json
import re

from django.core.exceptions import ValidationError, PermissionDenied
from django.http import Http404, JsonResponse
from django.utils import timezone

from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiTypes, OpenApiResponse, OpenApiParameter

from rest_framework import generics, views
from rest_framework.response import Response

from access.mixin import OrganizationMixin
from access.models import Organization

from api.views.mixin import OrganizationPermissionAPI
from api.serializers.itam.inventory import InventorySerializer
from api.serializers.inventory import Inventory

from core.http.common import Http

from itam.models.device import Device, DeviceType, DeviceOperatingSystem, DeviceSoftware
from itam.models.operating_system import OperatingSystem, OperatingSystemVersion
from itam.models.software import Software, SoftwareCategory, SoftwareVersion

from settings.models.app_settings import AppSettings
from settings.models.user_settings import UserSettings



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
            200: OpenApiResponse(description='Inventory updated an existing device'),
            201: OpenApiResponse(description='Inventory created a new device'),
            400: OpenApiResponse(description='Inventory is invalid'),
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

            device_operating_system = None
            operating_system = None
            operating_system_version = None


            app_settings = AppSettings.objects.get(owner_organization = None)

            if not device: # Create the device

                device = Device.objects.create(
                    name = data.details.name,
                    device_type = None,
                    serial_number = data.details.serial_number,
                    uuid = data.details.uuid,
                    organization = self.default_organization,
                )

                status = Http.Status.CREATED


            if not device.uuid and data.details.uuid:

                device.uuid = data.details.uuid

                device.save()


            if not device.serial_number and data.details.serial_number:

                device.serial_number = data.details.serial_number

                device.save()


            if OperatingSystem.objects.filter( slug=data.operating_system.name ).exists():

                operating_system = OperatingSystem.objects.get( slug=data.operating_system.name )

            else: # Create Operating System

                operating_system = OperatingSystem.objects.create(
                    name = data.operating_system.name,
                    organization = self.default_organization,
                    is_global = True
                )


            if OperatingSystemVersion.objects.filter( name=data.operating_system.version_major, operating_system=operating_system ).exists():

                operating_system_version = OperatingSystemVersion.objects.get(
                    organization = self.default_organization,
                    is_global = True,
                    name = data.operating_system.version_major,
                    operating_system = operating_system
                )

            else: # Create Operating System Version

                operating_system_version = OperatingSystemVersion.objects.create(
                    organization = self.default_organization,
                    is_global = True,
                    name = data.operating_system.version_major,
                    operating_system = operating_system,
                )


            if DeviceOperatingSystem.objects.filter( version=data.operating_system.version, device=device, operating_system_version=operating_system_version ).exists():

                device_operating_system = DeviceOperatingSystem.objects.get(
                    device=device,
                    version = data.operating_system.version,
                    operating_system_version = operating_system_version,
                )

                if not device_operating_system.installdate: # Only update install date if empty

                    device_operating_system.installdate = timezone.now()

                    device_operating_system.save()

            else: # Create Operating System Version

                device_operating_system = DeviceOperatingSystem.objects.create(
                    organization = self.default_organization,
                    device=device,
                    version = data.operating_system.version,
                    operating_system_version = operating_system_version,
                    installdate = timezone.now()
                )


            if app_settings.software_is_global:

                software_organization = app_settings.global_organization

            else:

                software_organization = device.organization

            
            if app_settings.software_categories_is_global:

                software_category_organization = app_settings.global_organization

            else:

                software_category_organization = device.organization



            for inventory in list(data.software):

                software = None
                software_category = None
                software_version = None

                device_software = None


                if SoftwareCategory.objects.filter( name = inventory.category ).exists():

                    software_category = SoftwareCategory.objects.get(
                        name = inventory.category
                    )

                else: # Create Software Category

                    software_category = SoftwareCategory.objects.create(
                        organization = software_category_organization,
                        is_global = True,
                        name = inventory.category,
                    )


                if Software.objects.filter( name = inventory.name ).exists():

                    software = Software.objects.get(
                        name = inventory.name
                    )

                    if not software.category:

                        software.category = software_category
                        software.save()

                else: # Create Software

                    software = Software.objects.create(
                        organization = software_organization,
                        is_global = True,
                        name = inventory.name,
                        category = software_category,
                    )


                pattern = r"^(\d+:)?(?P<semver>\d+\.\d+(\.\d+)?)"

                semver = re.search(pattern, str(inventory.version), re.DOTALL)


                if semver:

                    semver = semver['semver']

                else:
                    semver = inventory.version


                if SoftwareVersion.objects.filter( name = semver, software = software ).exists():

                    software_version = SoftwareVersion.objects.get(
                        name = semver,
                        software = software,
                    )

                else: # Create Software Category

                    software_version = SoftwareVersion.objects.create(
                        organization = self.default_organization,
                        is_global = True,
                        name = semver,
                        software = software,
                    )


                if DeviceSoftware.objects.filter( software = software, device=device ).exists():

                    device_software = DeviceSoftware.objects.get(
                        device = device,
                        software = software
                    )

                else: # Create Software

                    device_software = DeviceSoftware.objects.create(
                        organization = self.default_organization,
                        is_global = True,
                        installedversion = software_version,
                        software = software,
                        device = device,
                        action=None
                    )


                if device_software: # Update the Inventoried software

                    clear_installed_software = DeviceSoftware.objects.filter(
                        device = device,
                        software = software
                    )

                    # Clear installed version of all installed software
                    # any found later with no version to be removed
                    clear_installed_software.update(installedversion=None)


                    if not device_software.installed: # Only update install date if blank

                        device_software.installed = timezone.now()

                        device_software.save()

                    device_software.installedversion = software_version

                    device_software.save()


            if device and operating_system and operating_system_version and device_operating_system:

                # Remove software no longer installed
                DeviceSoftware.objects.filter(
                    device = device,
                    software = software,
                ).delete()

                device.inventorydate = timezone.now()

                device.save()

                if status != Http.Status.CREATED:

                    status = Http.Status.OK

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
