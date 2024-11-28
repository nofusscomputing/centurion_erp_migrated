import pytest
import unittest

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from rest_framework.relations import Hyperlink

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_fields import APITenancyObject

from core.models.manufacturer import Manufacturer

from itam.serializers.device_operating_system import Device, DeviceOperatingSystem, DeviceOperatingSystemModelSerializer
from itam.models.operating_system import OperatingSystem, OperatingSystemVersion



class OperatingSystemInstallsAPI(
    TestCase,
    APITenancyObject
):

    model = DeviceOperatingSystem

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create an item

        """

        self.organization = Organization.objects.create(name='test_org')

        # manufacturer = Manufacturer.objects.create(
        #     organization = self.organization,
        #     name = 'a manufacturer'
        # )

        # operating_system_version = SoftwareCategory.objects.create(
        #     organization = self.organization,
        #     name = 'operating_system_version'
        # )


        # software = Software.objects.create(
        #     organization = self.organization,
        #     name = 'one',
        #     publisher = manufacturer,
        #     operating_system_version = operating_system_version,
        #     model_notes = 'a note'
        # )

        # software_version = SoftwareVersion.objects.create(
        #     organization = self.organization,
        #     name = '10',
        #     software = software
        # )

        # device = Device.objects.create(
        #     organization = self.organization,
        #     name = 'device'
        # )

        # self.item = self.model.objects.create(
        #     organization = self.organization,
        #     device = device,
        #     software = software,
        #     version = software_version,
        #     installedversion = software_version,
        #     installed = '2024-01-01 01:00:00',
        #     action = DeviceOperatingSystem.Actions.INSTALL,
        #     model_notes = 'notes'

        # )

        self.operating_system = OperatingSystem.objects.create(
            organization=self.organization,
            name = '12',
        )

        self.operating_system_version = OperatingSystemVersion.objects.create(
            organization=self.organization,
            name = '12',
            operating_system = self.operating_system
        )

        self.device = Device.objects.create(
            organization=self.organization,
            name = 'device'
        )

        self.device_two = Device.objects.create(
            organization=self.organization,
            name = 'device-two'
        )


        self.item = self.model.objects.create(
            organization=self.organization,
            version = '1',
            operating_system_version = self.operating_system_version,
            device = self.device
        )


        self.url_view_kwargs = {'operating_system_id': self.operating_system_version.operating_system.id, 'pk': self.item.id}

        self.url_kwargs = {'operating_system_id':self.operating_system_version.operating_system.id}

        view_permissions = Permission.objects.get(
                codename = 'view_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        view_team = Team.objects.create(
            team_name = 'view_team',
            organization = self.organization,
        )

        view_team.permissions.set([view_permissions])

        self.view_user = User.objects.create_user(username="test_user_view", password="password")
        teamuser = TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )

        client = Client()
        url = reverse('v2:_api_v2_operating_system_installs-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data = response.data



    def test_api_field_exists_device(self):
        """ Test for existance of API Field

        device field must exist
        """

        assert 'device' in self.api_data


    def test_api_field_type_device(self):
        """ Test for type for API Field

        device field must be dict
        """

        assert type(self.api_data['device']) is dict


    def test_api_field_exists_device_id(self):
        """ Test for existance of API Field

        device.id field must exist
        """

        assert 'id' in self.api_data['device']


    def test_api_field_type_device_id(self):
        """ Test for type for API Field

        device.id field must be int
        """

        assert type(self.api_data['device']['id']) is int


    def test_api_field_exists_device_display_name(self):
        """ Test for existance of API Field

        device.display_name field must exist
        """

        assert 'display_name' in self.api_data['device']


    def test_api_field_type_device_display_name(self):
        """ Test for type for API Field

        device.display_name field must be str
        """

        assert type(self.api_data['device']['display_name']) is str


    def test_api_field_exists_device_url(self):
        """ Test for existance of API Field

        device.url field must exist
        """

        assert 'url' in self.api_data['device']


    def test_api_field_type_device_url(self):
        """ Test for type for API Field

        device.url field must be Hyperlink
        """

        assert type(self.api_data['device']['url']) is Hyperlink



    def test_api_field_exists_operating_system_version(self):
        """ Test for existance of API Field

        operating_system_version field must exist
        """

        assert 'operating_system_version' in self.api_data


    def test_api_field_type_operating_system_version(self):
        """ Test for type for API Field

        operating_system_version field must be dict
        """

        assert type(self.api_data['operating_system_version']) is dict


    def test_api_field_exists_operating_system_version_id(self):
        """ Test for existance of API Field

        operating_system_version.id field must exist
        """

        assert 'id' in self.api_data['operating_system_version']


    def test_api_field_type_operating_system_version_id(self):
        """ Test for type for API Field

        operating_system_version.id field must be int
        """

        assert type(self.api_data['operating_system_version']['id']) is int


    def test_api_field_exists_operating_system_version_display_name(self):
        """ Test for existance of API Field

        operating_system_version.display_name field must exist
        """

        assert 'display_name' in self.api_data['operating_system_version']


    def test_api_field_type_operating_system_version_display_name(self):
        """ Test for type for API Field

        operating_system_version.display_name field must be str
        """

        assert type(self.api_data['operating_system_version']['display_name']) is str


    def test_api_field_exists_operating_system_version_url(self):
        """ Test for existance of API Field

        operating_system_version.url field must exist
        """

        assert 'url' in self.api_data['operating_system_version']


    def test_api_field_type_operating_system_version_url(self):
        """ Test for type for API Field

        operating_system_version.url field must be Hyperlink
        """

        assert type(self.api_data['operating_system_version']['url']) is str



    def test_api_field_exists_display_name(self):
        """ Test for existance of API Field

        this test case is a custom test of a test with the same name.
        this model does not have a display_name field.

        display_name field must exist
        """

        assert 'display_name' not in self.api_data


    def test_api_field_type_display_name(self):
        """ Test for type for API Field

        this test case is a custom test of a test with the same name.
        this model does not have a display_name field.

        display_name field must be str
        """

        assert True



    def test_api_field_exists_model_notes(self):
        """ Test for existance of API Field

        this test case is a custom test of a test with the same name.
        this model does not have a model_notes field.

        model_notes field must exist
        """

        assert 'model_notes' not in self.api_data


    def test_api_field_type_model_notes(self):
        """ Test for type for API Field

        this test case is a custom test of a test with the same name.
        this model does not have a model_notes field.

        model_notes field must be str
        """

        assert True



    def test_api_field_exists_version(self):
        """ Test for existance of API Field

        version field must exist
        """

        assert 'version' in self.api_data


    def test_api_field_type_version(self):
        """ Test for type for API Field

        version field must be dict
        """

        assert type(self.api_data['version']) is str
