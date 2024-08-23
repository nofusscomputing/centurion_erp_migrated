import datetime
import json
import pytest
import unittest

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import TestCase, Client
from django.test.utils import override_settings

from unittest.mock import patch

from access.models import Organization, Team, TeamUsers, Permission

from api.views.mixin import OrganizationPermissionAPI
from api.serializers.inventory import Inventory

from api.tasks import process_inventory

from itam.models.device import Device, DeviceOperatingSystem, DeviceSoftware
from itam.models.operating_system import OperatingSystem, OperatingSystemVersion
from itam.models.software import Software, SoftwareCategory, SoftwareVersion

from settings.models.user_settings import UserSettings



class InventoryAPI(TestCase):

    model = Device

    model_name = 'device'
    app_label = 'itam'

    inventory = {
        "details": {
            "name": "device_name",
            "serial_number": "a serial number",
            "uuid": "string"
        },
        "os": {
            "name": "os_name",
            "version_major": "12",
            "version": "12.1"
        },
        "software": [
            {
                "name": "software_name",
                "category": "category_name",
                "version": "1.2.3"
            },
            {
                "name": "software_name_not_semver",
                "category": "category_name",
                "version": "2024.4"
            },
            {
                "name": "software_name_semver_contained",
                "category": "category_name",
                "version": "1.2.3-rc1"
            },
        ]
    }



    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user
        2. Create a team for user with correct permissions
        3. add user to the teeam
        4. upload the inventory
        5. conduct queries for tests
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        add_permissions = Permission.objects.get(
                codename = 'add_' + self.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.app_label,
                    model = self.model_name,
                )
            )

        add_team = Team.objects.create(
            team_name = 'add_team',
            organization = organization,
        )

        add_team.permissions.set([add_permissions])

        self.add_user = User.objects.create_user(username="test_user_add", password="password")

        add_user_settings = UserSettings.objects.get(user=self.add_user)

        add_user_settings.default_organization = organization

        add_user_settings.save()

        teamuser = TeamUsers.objects.create(
            team = add_team,
            user = self.add_user
        )

        # upload the inventory
        process_inventory(json.dumps(self.inventory), organization.id)


        self.device = Device.objects.get(name=self.inventory['details']['name'])

        self.operating_system = OperatingSystem.objects.get(name=self.inventory['os']['name'])

        self.operating_system_version = OperatingSystemVersion.objects.get(name=self.inventory['os']['version_major'])

        self.device_operating_system = DeviceOperatingSystem.objects.get(version=self.inventory['os']['version'])

        self.software = Software.objects.get(name=self.inventory['software'][0]['name'])

        self.software_category = SoftwareCategory.objects.get(name=self.inventory['software'][0]['category'])

        self.software_version = SoftwareVersion.objects.get(
            name = self.inventory['software'][0]['version'],
            software = self.software,
        )

        self.software_not_semver = Software.objects.get(name=self.inventory['software'][1]['name'])

        self.software_version_not_semver = SoftwareVersion.objects.get(
            name = self.inventory['software'][1]['version'],
            software = self.software_not_semver
        )

        self.software_is_semver = Software.objects.get(name=self.inventory['software'][2]['name'])

        self.software_version_is_semver = SoftwareVersion.objects.get(
            software = self.software_is_semver
        )

        self.device_software = DeviceSoftware.objects.get(device=self.device,software=self.software)




    @override_settings(CELERY_TASK_ALWAYS_EAGER=True,
                       CELERY_TASK_EAGER_PROPOGATES=True)
    @patch.object(OrganizationPermissionAPI, 'permission_check')
    def test_inventory_function_called_permission_check(self, permission_check):
        """ Inventory Upload checks permissions
        
        Function 'permission_check' is the function that checks permissions

        As the non-established way of authentication an API permission is being done
        confimation that the permissions are still checked is required.
        """

        client = Client()
        url = reverse('API:_api_device_inventory')

        client.force_login(self.add_user)
        response = client.post(url, data=self.inventory, content_type='application/json')

        assert permission_check.called



    @override_settings(CELERY_TASK_ALWAYS_EAGER=True,
                       CELERY_TASK_EAGER_PROPOGATES=True)
    @patch.object(Inventory, '__init__')
    def test_inventory_serializer_inventory_called(self, serializer):
        """ Inventory Upload checks permissions
        
        Function 'permission_check' is the function that checks permissions

        As the non-established way of authentication an API permission is being done
        confimation that the permissions are still checked is required.
        """

        client = Client()
        url = reverse('API:_api_device_inventory')

        client.force_login(self.add_user)
        response = client.post(url, data=self.inventory, content_type='application/json')

        assert serializer.called



    @override_settings(CELERY_TASK_ALWAYS_EAGER=True,
                       CELERY_TASK_EAGER_PROPOGATES=True)
    @patch.object(Inventory.Details, '__init__')
    def test_inventory_serializer_inventory_details_called(self, serializer):
        """ Inventory Upload uses Inventory serializer

        Details Serializer is called for inventory details dict.
        """

        client = Client()
        url = reverse('API:_api_device_inventory')

        client.force_login(self.add_user)
        response = client.post(url, data=self.inventory, content_type='application/json')

        assert serializer.called



    @override_settings(CELERY_TASK_ALWAYS_EAGER=True,
                       CELERY_TASK_EAGER_PROPOGATES=True)
    @patch.object(Inventory.OperatingSystem, '__init__')
    def test_inventory_serializer_inventory_operating_system_called(self, serializer):
        """ Inventory Upload uses Inventory serializer

        Operating System Serializer is called for inventory Operating system dict.
        """

        client = Client()
        url = reverse('API:_api_device_inventory')

        client.force_login(self.add_user)
        response = client.post(url, data=self.inventory, content_type='application/json')

        assert serializer.called



    @override_settings(CELERY_TASK_ALWAYS_EAGER=True,
                       CELERY_TASK_EAGER_PROPOGATES=True)
    @patch.object(Inventory.Software, '__init__')
    def test_inventory_serializer_inventory_software_called(self, serializer):
        """ Inventory Upload uses Inventory serializer

        Software Serializer is called for inventory software list.
        """

        client = Client()
        url = reverse('API:_api_device_inventory')

        client.force_login(self.add_user)
        response = client.post(url, data=self.inventory, content_type='application/json')

        assert serializer.called



    def test_api_inventory_device_added(self):
        """ Device is created """

        assert self.device.name == self.inventory['details']['name']



    def test_api_inventory_device_uuid_match(self):
        """ Device uuid match """

        assert self.device.uuid == self.inventory['details']['uuid']



    def test_api_inventory_device_serial_number_match(self):
        """ Device SN match """

        assert self.device.serial_number == self.inventory['details']['serial_number']



    def test_api_inventory_operating_system_added(self):
        """ Operating System is created """

        assert self.operating_system.name == self.inventory['os']['name']



    def test_api_inventory_operating_system_version_added(self):
        """ Operating System version is created """

        assert self.operating_system_version.name == self.inventory['os']['version_major']



    def test_api_inventory_device_has_operating_system_added(self):
        """ Operating System version linked to device """

        assert self.device_operating_system.version == self.inventory['os']['version']



    @pytest.mark.skip(reason="to be written")
    def test_api_inventory_device_operating_system_version_is_semver(self):
        """ Operating System version is full semver
        
            Operating system versions name is the major version number of semver.
            The device version is to be full semver 
        """
        pass



    @pytest.mark.skip(reason="to be written")
    def test_api_inventory_software_no_version_cleaned(self):
        """ Check softare cleaned up
        
        As part of the inventory upload the software versions of software found on the device is set to null
        and before the processing is completed, the version=null software is supposed to be cleaned up.
        """
        pass



    def test_api_inventory_software_category_added(self):
        """ Software category exists """

        assert self.software_category.name == self.inventory['software'][0]['category']



    def test_api_inventory_software_added(self):
        """ Test software exists """

        assert self.software.name == self.inventory['software'][0]['name']



    def test_api_inventory_software_category_linked_to_software(self):
        """ Software category linked to software """

        assert self.software.category == self.software_category



    def test_api_inventory_software_version_added(self):
        """ Test software version exists """

        assert self.software_version.name == self.inventory['software'][0]['version']



    def test_api_inventory_software_version_returns_semver(self):
        """ Software Version from inventory returns semver if within version string """
        
        assert self.software_version_is_semver.name == str(self.inventory['software'][2]['version']).split('-')[0]



    def test_api_inventory_software_version_returns_original_version(self):
        """ Software Version from inventory returns inventoried version if no semver found """

        assert self.software_version_not_semver.name == self.inventory['software'][1]['version']




    def test_api_inventory_software_version_linked_to_software(self):
        """ Test software version linked to software it belongs too """

        assert self.software_version.software == self.software



    def test_api_inventory_device_has_software_version(self):
        """ Inventoried software is linked to device and it's the corret one"""

        assert self.software_version.name == self.inventory['software'][0]['version']



    def test_api_inventory_device_software_has_installed_date(self):
        """ Inventoried software version has install date """

        assert self.device_software.installed is not None



    def test_api_inventory_device_software_installed_date_type(self):
        """ Inventoried software version has install date """

        assert type(self.device_software.installed) is datetime.datetime



    @pytest.mark.skip(reason="to be written")
    def test_api_inventory_device_software_blank_installed_date_is_updated(self):
        """ A blank installed date of software is updated if the software was already attached to the device """
        pass


    @override_settings(CELERY_TASK_ALWAYS_EAGER=True,
                       CELERY_TASK_EAGER_PROPOGATES=True)
    def test_api_inventory_valid_status_ok_existing_device(self):
        """ Successful inventory upload returns 200 for existing device"""

        client = Client()
        url = reverse('API:_api_device_inventory')

        client.force_login(self.add_user)
        response = client.post(url, data=self.inventory, content_type='application/json')

        assert response.status_code == 200


    @override_settings(CELERY_TASK_ALWAYS_EAGER=True,
                       CELERY_TASK_EAGER_PROPOGATES=True)
    def test_api_inventory_invalid_status_bad_request(self):
        """ Incorrectly formated inventory upload returns 400 """

        client = Client()
        url = reverse('API:_api_device_inventory')

        mod_inventory = self.inventory.copy()

        mod_inventory.update({
            'details': {
                'name': 'test_api_inventory_invalid_status_bad_request'
            },
            'software': {
                'not_within_a': 'list'
            }
        })

        client.force_login(self.add_user)
        response = client.post(url, data=mod_inventory, content_type='application/json')

        assert response.status_code == 400



    @pytest.mark.skip(reason="to be written")
    def test_api_inventory_exeception_status_sever_error(self):
        """ if the method throws an exception 500 must be returned.
        
        idea to test: add a random key to the report that is not documented
        and perform some action against it that will cause a python exception.
        """
        pass





class InventoryAPIDifferentNameSerialNumberMatch(TestCase):
    """ Test inventory upload with different name

    should match by serial number
    """

    model = Device

    model_name = 'device'
    app_label = 'itam'

    inventory = {
        "details": {
            "name": "device_name",
            "serial_number": "serial_number_123",
            "uuid": "string"
        },
        "os": {
            "name": "os_name",
            "version_major": "12",
            "version": "12.1"
        },
        "software": [
            {
                "name": "software_name",
                "category": "category_name",
                "version": "1.2.3"
            },
            {
                "name": "software_name_not_semver",
                "category": "category_name",
                "version": "2024.4"
            },
            {
                "name": "software_name_semver_contained",
                "category": "category_name",
                "version": "1.2.3-rc1"
            },
        ]
    }



    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user
        2. Create a team for user with correct permissions
        3. add user to the teeam
        4. upload the inventory
        5. conduct queries for tests
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        Device.objects.create(
            name='random device name',
            serial_number='serial_number_123'
        )

        add_permissions = Permission.objects.get(
                codename = 'add_' + self.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.app_label,
                    model = self.model_name,
                )
            )

        add_team = Team.objects.create(
            team_name = 'add_team',
            organization = organization,
        )

        add_team.permissions.set([add_permissions])

        self.add_user = User.objects.create_user(username="test_user_add", password="password")

        add_user_settings = UserSettings.objects.get(user=self.add_user)

        add_user_settings.default_organization = organization

        add_user_settings.save()

        teamuser = TeamUsers.objects.create(
            team = add_team,
            user = self.add_user
        )

        # upload the inventory
        process_inventory(json.dumps(self.inventory), organization.id)


        self.device = Device.objects.get(name=self.inventory['details']['name'])

        self.operating_system = OperatingSystem.objects.get(name=self.inventory['os']['name'])

        self.operating_system_version = OperatingSystemVersion.objects.get(name=self.inventory['os']['version_major'])

        self.device_operating_system = DeviceOperatingSystem.objects.get(version=self.inventory['os']['version'])

        self.software = Software.objects.get(name=self.inventory['software'][0]['name'])

        self.software_category = SoftwareCategory.objects.get(name=self.inventory['software'][0]['category'])

        self.software_version = SoftwareVersion.objects.get(
            name = self.inventory['software'][0]['version'],
            software = self.software,
        )

        self.software_not_semver = Software.objects.get(name=self.inventory['software'][1]['name'])

        self.software_version_not_semver = SoftwareVersion.objects.get(
            name = self.inventory['software'][1]['version'],
            software = self.software_not_semver
        )

        self.software_is_semver = Software.objects.get(name=self.inventory['software'][2]['name'])

        self.software_version_is_semver = SoftwareVersion.objects.get(
            software = self.software_is_semver
        )

        self.device_software = DeviceSoftware.objects.get(device=self.device,software=self.software)



    def test_api_inventory_device_added(self):
        """ Device is created """

        assert self.device.name == self.inventory['details']['name']



    def test_api_inventory_device_uuid_match(self):
        """ Device uuid match """

        assert self.device.uuid == self.inventory['details']['uuid']



    def test_api_inventory_device_serial_number_match(self):
        """ Device SN match """

        assert self.device.serial_number == self.inventory['details']['serial_number']



    def test_api_inventory_operating_system_added(self):
        """ Operating System is created """

        assert self.operating_system.name == self.inventory['os']['name']



    def test_api_inventory_operating_system_version_added(self):
        """ Operating System version is created """

        assert self.operating_system_version.name == self.inventory['os']['version_major']



    def test_api_inventory_device_has_operating_system_added(self):
        """ Operating System version linked to device """

        assert self.device_operating_system.version == self.inventory['os']['version']



    @pytest.mark.skip(reason="to be written")
    def test_api_inventory_device_operating_system_version_is_semver(self):
        """ Operating System version is full semver
        
            Operating system versions name is the major version number of semver.
            The device version is to be full semver 
        """
        pass



    @pytest.mark.skip(reason="to be written")
    def test_api_inventory_software_no_version_cleaned(self):
        """ Check softare cleaned up
        
        As part of the inventory upload the software versions of software found on the device is set to null
        and before the processing is completed, the version=null software is supposed to be cleaned up.
        """
        pass



    def test_api_inventory_software_category_added(self):
        """ Software category exists """

        assert self.software_category.name == self.inventory['software'][0]['category']



    def test_api_inventory_software_added(self):
        """ Test software exists """

        assert self.software.name == self.inventory['software'][0]['name']



    def test_api_inventory_software_category_linked_to_software(self):
        """ Software category linked to software """

        assert self.software.category == self.software_category



    def test_api_inventory_software_version_added(self):
        """ Test software version exists """

        assert self.software_version.name == self.inventory['software'][0]['version']



    def test_api_inventory_software_version_returns_semver(self):
        """ Software Version from inventory returns semver if within version string """
        
        assert self.software_version_is_semver.name == str(self.inventory['software'][2]['version']).split('-')[0]



    def test_api_inventory_software_version_returns_original_version(self):
        """ Software Version from inventory returns inventoried version if no semver found """

        assert self.software_version_not_semver.name == self.inventory['software'][1]['version']




    def test_api_inventory_software_version_linked_to_software(self):
        """ Test software version linked to software it belongs too """

        assert self.software_version.software == self.software



    def test_api_inventory_device_has_software_version(self):
        """ Inventoried software is linked to device and it's the corret one"""

        assert self.software_version.name == self.inventory['software'][0]['version']



    def test_api_inventory_device_software_has_installed_date(self):
        """ Inventoried software version has install date """

        assert self.device_software.installed is not None



    def test_api_inventory_device_software_installed_date_type(self):
        """ Inventoried software version has install date """

        assert type(self.device_software.installed) is datetime.datetime



    @pytest.mark.skip(reason="to be written")
    def test_api_inventory_device_software_blank_installed_date_is_updated(self):
        """ A blank installed date of software is updated if the software was already attached to the device """
        pass








class InventoryAPIDifferentNameUUIDMatch(TestCase):
    """ Test inventory upload with different name

    should match by uuid
    """

    model = Device

    model_name = 'device'
    app_label = 'itam'

    inventory = {
        "details": {
            "name": "device_name",
            "serial_number": "serial_number_123",
            "uuid": "123-456-789"
        },
        "os": {
            "name": "os_name",
            "version_major": "12",
            "version": "12.1"
        },
        "software": [
            {
                "name": "software_name",
                "category": "category_name",
                "version": "1.2.3"
            },
            {
                "name": "software_name_not_semver",
                "category": "category_name",
                "version": "2024.4"
            },
            {
                "name": "software_name_semver_contained",
                "category": "category_name",
                "version": "1.2.3-rc1"
            },
        ]
    }



    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user
        2. Create a team for user with correct permissions
        3. add user to the teeam
        4. upload the inventory
        5. conduct queries for tests
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        Device.objects.create(
            name='random device name',
            uuid='123-456-789'
        )

        add_permissions = Permission.objects.get(
                codename = 'add_' + self.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.app_label,
                    model = self.model_name,
                )
            )

        add_team = Team.objects.create(
            team_name = 'add_team',
            organization = organization,
        )

        add_team.permissions.set([add_permissions])

        self.add_user = User.objects.create_user(username="test_user_add", password="password")

        add_user_settings = UserSettings.objects.get(user=self.add_user)

        add_user_settings.default_organization = organization

        add_user_settings.save()

        teamuser = TeamUsers.objects.create(
            team = add_team,
            user = self.add_user
        )

        # upload the inventory
        process_inventory(json.dumps(self.inventory), organization.id)


        self.device = Device.objects.get(name=self.inventory['details']['name'])

        self.operating_system = OperatingSystem.objects.get(name=self.inventory['os']['name'])

        self.operating_system_version = OperatingSystemVersion.objects.get(name=self.inventory['os']['version_major'])

        self.device_operating_system = DeviceOperatingSystem.objects.get(version=self.inventory['os']['version'])

        self.software = Software.objects.get(name=self.inventory['software'][0]['name'])

        self.software_category = SoftwareCategory.objects.get(name=self.inventory['software'][0]['category'])

        self.software_version = SoftwareVersion.objects.get(
            name = self.inventory['software'][0]['version'],
            software = self.software,
        )

        self.software_not_semver = Software.objects.get(name=self.inventory['software'][1]['name'])

        self.software_version_not_semver = SoftwareVersion.objects.get(
            name = self.inventory['software'][1]['version'],
            software = self.software_not_semver
        )

        self.software_is_semver = Software.objects.get(name=self.inventory['software'][2]['name'])

        self.software_version_is_semver = SoftwareVersion.objects.get(
            software = self.software_is_semver
        )

        self.device_software = DeviceSoftware.objects.get(device=self.device,software=self.software)



    def test_api_inventory_device_added(self):
        """ Device is created """

        assert self.device.name == self.inventory['details']['name']



    def test_api_inventory_device_uuid_match(self):
        """ Device uuid match """

        assert self.device.uuid == self.inventory['details']['uuid']



    def test_api_inventory_device_serial_number_match(self):
        """ Device SN match """

        assert self.device.serial_number == self.inventory['details']['serial_number']



    def test_api_inventory_operating_system_added(self):
        """ Operating System is created """

        assert self.operating_system.name == self.inventory['os']['name']



    def test_api_inventory_operating_system_version_added(self):
        """ Operating System version is created """

        assert self.operating_system_version.name == self.inventory['os']['version_major']



    def test_api_inventory_device_has_operating_system_added(self):
        """ Operating System version linked to device """

        assert self.device_operating_system.version == self.inventory['os']['version']



    @pytest.mark.skip(reason="to be written")
    def test_api_inventory_device_operating_system_version_is_semver(self):
        """ Operating System version is full semver
        
            Operating system versions name is the major version number of semver.
            The device version is to be full semver 
        """
        pass



    @pytest.mark.skip(reason="to be written")
    def test_api_inventory_software_no_version_cleaned(self):
        """ Check softare cleaned up
        
        As part of the inventory upload the software versions of software found on the device is set to null
        and before the processing is completed, the version=null software is supposed to be cleaned up.
        """
        pass



    def test_api_inventory_software_category_added(self):
        """ Software category exists """

        assert self.software_category.name == self.inventory['software'][0]['category']



    def test_api_inventory_software_added(self):
        """ Test software exists """

        assert self.software.name == self.inventory['software'][0]['name']



    def test_api_inventory_software_category_linked_to_software(self):
        """ Software category linked to software """

        assert self.software.category == self.software_category



    def test_api_inventory_software_version_added(self):
        """ Test software version exists """

        assert self.software_version.name == self.inventory['software'][0]['version']



    def test_api_inventory_software_version_returns_semver(self):
        """ Software Version from inventory returns semver if within version string """
        
        assert self.software_version_is_semver.name == str(self.inventory['software'][2]['version']).split('-')[0]



    def test_api_inventory_software_version_returns_original_version(self):
        """ Software Version from inventory returns inventoried version if no semver found """

        assert self.software_version_not_semver.name == self.inventory['software'][1]['version']




    def test_api_inventory_software_version_linked_to_software(self):
        """ Test software version linked to software it belongs too """

        assert self.software_version.software == self.software



    def test_api_inventory_device_has_software_version(self):
        """ Inventoried software is linked to device and it's the corret one"""

        assert self.software_version.name == self.inventory['software'][0]['version']



    def test_api_inventory_device_software_has_installed_date(self):
        """ Inventoried software version has install date """

        assert self.device_software.installed is not None



    def test_api_inventory_device_software_installed_date_type(self):
        """ Inventoried software version has install date """

        assert type(self.device_software.installed) is datetime.datetime



    @pytest.mark.skip(reason="to be written")
    def test_api_inventory_device_software_blank_installed_date_is_updated(self):
        """ A blank installed date of software is updated if the software was already attached to the device """
        pass

