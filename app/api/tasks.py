import json
import re

from django.utils import timezone

from celery import shared_task, current_task
from celery.utils.log import get_task_logger
from celery import states

from access.models import Organization

from api.serializers.inventory import Inventory

from itam.models.device import Device, DeviceType, DeviceOperatingSystem, DeviceSoftware
from itam.models.operating_system import OperatingSystem, OperatingSystemVersion
from itam.models.software import Software, SoftwareCategory, SoftwareVersion

from settings.models.app_settings import AppSettings


logger = get_task_logger(__name__)

@shared_task(bind=True)
def process_inventory(self, data, organization: int):

    device = None
    device_operating_system = None
    operating_system = None
    operating_system_version = None

    try:

        logger.info('Begin Processing Inventory')

        data = json.loads(data)
        data = Inventory(data)

        organization = Organization.objects.get(id=organization)

        app_settings = AppSettings.objects.get(owner_organization = None)

        device_serial_number = None
        device_uuid = None

        if data.details.serial_number and str(data.details.serial_number).lower() != 'na':

            device_serial_number = str(data.details.serial_number)

        if data.details.uuid and str(data.details.uuid).lower() != 'na':

            device_uuid = str(data.details.uuid)


        if device_serial_number: # Search for device by serial number.

            device = Device.objects.filter(
                serial_number__iexact=device_serial_number
            )

            if device.exists():

                device = Device.objects.get(
                    serial_number__iexact=device_serial_number
                )

            else:

                device = None


        if device_uuid and not device: # Search for device by UUID.

            device = Device.objects.filter(
                uuid__iexact=device_uuid
            )

            if device.exists():

                device = Device.objects.get(
                    uuid__iexact=device_uuid
                )

            else:

                device = None


        if not device: # Search for device by Name.

            device = Device.objects.filter(
                name__iexact=str(data.details.name).lower()
            )

            if device.exists():

                device = Device.objects.get(
                    name__iexact=str(data.details.name).lower()
                )

            else:

                device = None




        if not device: # Create the device

            device = Device.objects.create(
                name = data.details.name,
                device_type = None,
                serial_number = device_serial_number,
                uuid = device_uuid,
                organization = organization,
            )


        if device:

            logger.info(f"Device: {device.name}, Serial: {device.serial_number}, UUID: {device.uuid}")

            device_edited = False


            if not device.uuid and device_uuid:

                device.uuid = device_uuid

                device_edited = True


            if not device.serial_number and device_serial_number:

                device.serial_number = data.details.serial_number

                device_edited = True


            if str(device.name).lower() != str(data.details.name).lower(): # Update device Name

                device.name = data.details.name

                device_edited = True


            if device_edited:

                device.save()


            operating_system = OperatingSystem.objects.filter(
                name=data.operating_system.name,
                is_global = True
            )

            if operating_system.exists():

                operating_system = OperatingSystem.objects.get(
                    name=data.operating_system.name,
                    is_global = True
                )


            else:

                operating_system = None



            if not operating_system:

                operating_system = OperatingSystem.objects.filter(
                    name=data.operating_system.name,
                    organization = organization
                )


                if operating_system.exists():

                    operating_system = OperatingSystem.objects.get(
                        name=data.operating_system.name,
                        organization = organization
                    )

                else:

                    operating_system = None


            if not operating_system:

                operating_system = OperatingSystem.objects.create(
                    name = data.operating_system.name,
                    organization = organization,
                    is_global = True
                )


            operating_system_version = OperatingSystemVersion.objects.filter(
                name=data.operating_system.version_major,
                operating_system=operating_system
            )

            if operating_system_version.exists():

                operating_system_version = OperatingSystemVersion.objects.get(
                    name=data.operating_system.version_major,
                    operating_system=operating_system
                )

            else:

                operating_system_version = None


            if not operating_system_version:

                operating_system_version = OperatingSystemVersion.objects.create(
                    organization = organization,
                    is_global = True,
                    name = data.operating_system.version_major,
                    operating_system = operating_system,
                )

            device_operating_system = DeviceOperatingSystem.objects.filter(
                device=device,
            )

            if device_operating_system.exists():

                device_operating_system = DeviceOperatingSystem.objects.get(
                    device=device,
                )

            else:

                device_operating_system = None


            if not device_operating_system:

                device_operating_system = DeviceOperatingSystem.objects.create(
                    organization = organization,
                    device=device,
                    version = data.operating_system.version,
                    operating_system_version = operating_system_version,
                    installdate = timezone.now()
                )

            if not device_operating_system.installdate: # Only update install date if empty

                device_operating_system.installdate = timezone.now()

                device_operating_system.save()


            if device_operating_system.operating_system_version != operating_system_version:

                device_operating_system.operating_system_version = operating_system_version

                device_operating_system.save()


            if device_operating_system.version != data.operating_system.version:

                device_operating_system.version = data.operating_system.version

                device_operating_system.save()


            if app_settings.software_is_global:

                software_organization = app_settings.global_organization

            else:

                software_organization = device.organization

            
            if app_settings.software_categories_is_global:

                software_category_organization = app_settings.global_organization

            else:

                software_category_organization = device.organization

            inventoried_software: list = []

            for inventory in list(data.software):

                software = None
                software_category = None
                software_version = None

                device_software = None

                software_category = SoftwareCategory.objects.filter( name = inventory.category )


                if software_category.exists():

                    software_category = SoftwareCategory.objects.get(
                        name = inventory.category
                    )

                else: # Create Software Category

                    software_category = SoftwareCategory.objects.create(
                        organization = software_category_organization,
                        is_global = True,
                        name = inventory.category,
                    )


                if software_category.name == inventory.category:

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


                    if software.name == inventory.name:

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
                                organization = organization,
                                is_global = True,
                                name = semver,
                                software = software,
                            )


                        if software_version.name == semver:

                            if DeviceSoftware.objects.filter( software = software, device=device ).exists():

                                device_software = DeviceSoftware.objects.get(
                                    device = device,
                                    software = software
                                )

                                logger.debug(f"Select Existing Device Software: {device_software.software.name}")

                            else: # Create Software

                                device_software = DeviceSoftware.objects.create(
                                    organization = organization,
                                    is_global = True,
                                    installedversion = software_version,
                                    software = software,
                                    device = device,
                                    action=None
                                )


                                logger.debug(f"Create Device Software: {device_software.software.name}")


                            if device_software: # Update the Inventoried software

                                inventoried_software += [ device_software.id ]


                                if not device_software.installed: # Only update install date if blank

                                    device_software.installed = timezone.now()

                                    device_software.save()

                                    logger.debug(f"Update Device Software (installed): {device_software.software.name}")


                                if device_software.installedversion.name != software_version.name:

                                    device_software.installedversion = software_version

                                    device_software.save()

                                    logger.debug(f"Update Device Software (installedversion): {device_software.software.name}")

            for not_installed in DeviceSoftware.objects.filter( device=device ):

                if not_installed.id not in inventoried_software:

                    not_installed.delete()

                    logger.debug(f"Remove Device Software: {not_installed.software.name}")


            if device and operating_system and operating_system_version and device_operating_system:


                device.inventorydate = timezone.now()

                device.save()


        logger.info('Finish Processing Inventory')

        return str('finished...')

    except Exception as e:
        
        logger.critical('Exception')

        raise Exception(e)

        return str(f'Exception Occured: {e}')
