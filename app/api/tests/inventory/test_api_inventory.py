import pytest
import unittest

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import TestCase, Client

from unittest.mock import patch

from access.models import Organization, Team, TeamUsers, Permission

from api.views.mixin import OrganizationPermissionAPI

from itam.models.device import Device

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
            }
        ]
    }



    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a device
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
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


    @pytest.mark.skip(reason="to be written")
    def test_api_inventory_device_added(self):
        """ Device is created """
        pass



    @pytest.mark.skip(reason="to be written")
    def test_api_inventory_operating_system_added(self):
        """ Operating System is created """
        pass



    @pytest.mark.skip(reason="to be written")
    def test_api_inventory_operating_system_version_added(self):
        """ Operating System version is created """
        pass



    @pytest.mark.skip(reason="to be written")
    def test_api_inventory_device_has_operating_system_added(self):
        """ Operating System version linked to device """
        pass



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



    @pytest.mark.skip(reason="to be written")
    def test_api_inventory_software_category_added(self):
        """ Software category exists """
        pass



    @pytest.mark.skip(reason="to be written")
    def test_api_inventory_software_added(self):
        """ Test software exists """
        pass



    @pytest.mark.skip(reason="to be written")
    def test_api_inventory_software_category_linked_to_software(self):
        """ Software category linked to software """
        pass



    @pytest.mark.skip(reason="to be written")
    def test_api_inventory_software_version_added(self):
        """ Test software version exists """
        pass



    @pytest.mark.skip(reason="to be written")
    def test_api_inventory_software_version_returns_semver(self):
        """ Software Version from inventory returns semver if within version string """
        pass



    @pytest.mark.skip(reason="to be written")
    def test_api_inventory_software_version_returns_original_version(self):
        """ Software Version from inventory returns inventoried version if no semver found """
        pass



    @pytest.mark.skip(reason="to be written")
    def test_api_inventory_software_version_linked_to_software(self):
        """ Test software version linked to software it belongs too """
        pass



    @pytest.mark.skip(reason="to be written")
    def test_api_inventory_device_has_software_version(self):
        """ Inventoried software is linked to device and it's the corret one"""
        pass



    @pytest.mark.skip(reason="to be written")
    def test_api_inventory_device_software_has_installed_date(self):
        """ Inventoried software version has install date """
        pass



    @pytest.mark.skip(reason="to be written")
    def test_api_inventory_device_software_blank_installed_date_is_updated(self):
        """ A blank installed date of software is updated if the software was already attached to the device """
        pass



    @pytest.mark.skip(reason="to be written")
    def test_api_inventory_valid_status_created(self):
        """ Successful inventory upload returns 201 """
        pass



    @pytest.mark.skip(reason="to be written")
    def test_api_inventory_invalid_status_bad_request(self):
        """ Incorrectly formated inventory upload returns 400 """
        pass



    @pytest.mark.skip(reason="to be written")
    def test_api_inventory_exeception_status_sever_error(self):
        """ if the method throws an exception 500 must be returned.
        
        idea to test: add a random key to the report that is not documented
        and perform some action against it that will cause a python exception.
        """
        pass

