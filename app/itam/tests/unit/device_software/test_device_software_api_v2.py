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

from itam.models.device import Device, DeviceSoftware
from itam.models.software import Software, SoftwareCategory, SoftwareVersion



class DeviceSoftwareAPI(
    TestCase,
    APITenancyObject
):

    model = DeviceSoftware

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create an item

        """

        self.organization = Organization.objects.create(name='test_org')

        manufacturer = Manufacturer.objects.create(
            organization = self.organization,
            name = 'a manufacturer'
        )

        category = SoftwareCategory.objects.create(
            organization = self.organization,
            name = 'category'
        )


        software = Software.objects.create(
            organization = self.organization,
            name = 'one',
            publisher = manufacturer,
            category = category,
            model_notes = 'a note'
        )

        software_version = SoftwareVersion.objects.create(
            organization = self.organization,
            name = '10',
            software = software
        )

        device = Device.objects.create(
            organization = self.organization,
            name = 'device'
        )

        self.item = self.model.objects.create(
            organization = self.organization,
            device = device,
            software = software,
            version = software_version,
            installedversion = software_version,
            installed = '2024-01-01 01:00:00',
            action = DeviceSoftware.Actions.INSTALL,
            model_notes = 'notes'

        )


        self.url_view_kwargs = {'device_id': device.id, 'pk': self.item.id}

        self.url_kwargs = {'deice_id': device.id}

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
        url = reverse('v2:_api_v2_device_software-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data = response.data



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



    def test_api_field_exists_action(self):
        """ Test for existance of API Field

        action field must exist
        """

        assert 'action' in self.api_data


    def test_api_field_type_action(self):
        """ Test for type for API Field

        action field must be int
        """

        assert type(self.api_data['action']) is int



    def test_api_field_exists_installed(self):
        """ Test for existance of API Field

        installed field must exist
        """

        assert 'installed' in self.api_data


    def test_api_field_type_installed(self):
        """ Test for type for API Field

        installed field must be str
        """

        assert type(self.api_data['installed']) is str



    def test_api_field_exists_action_badge(self):
        """ Test for existance of API Field

        action_badge field must exist
        """

        assert 'action_badge' in self.api_data


    def test_api_field_type_action_badge(self):
        """ Test for type for API Field

        action_badge field must be dict
        """

        assert type(self.api_data['action_badge']) is dict



    def test_api_field_exists_action_badge_icon(self):
        """ Test for existance of API Field

        action_badge.icon field must exist
        """

        assert 'icon' in self.api_data['action_badge']


    def test_api_field_type_action_badge(self):
        """ Test for type for API Field

        action_badge.icon field must be dict
        """

        assert type(self.api_data['action_badge']['icon']) is dict



    def test_api_field_exists_action_badge_icon_name(self):
        """ Test for existance of API Field

        action_badge.icon.name field must exist
        """

        assert 'name' in self.api_data['action_badge']['icon']


    def test_api_field_type_action_badge_icon_name(self):
        """ Test for type for API Field

        action_badge.icon.name field must be str
        """

        assert type(self.api_data['action_badge']['icon']['name']) is str



    def test_api_field_exists_action_badge_icon_style(self):
        """ Test for existance of API Field

        action_badge.icon.style field must exist
        """

        assert 'style' in self.api_data['action_badge']['icon']


    def test_api_field_type_action_badge_icon_style(self):
        """ Test for type for API Field

        action_badge.icon.style field must be str
        """

        assert type(self.api_data['action_badge']['icon']['style']) is str



    def test_api_field_exists_action_badge_text(self):
        """ Test for existance of API Field

        action_badge.text field must exist
        """

        assert 'text' in self.api_data['action_badge']


    def test_api_field_type_action_text(self):
        """ Test for type for API Field

        action_badge.text field must be str
        """

        assert type(self.api_data['action_badge']['text']) is str


    def test_api_field_exists_action_badge_text_style(self):
        """ Test for existance of API Field

        action_badge.text_style field must exist
        """

        assert 'text_style' in self.api_data['action_badge']


    def test_api_field_type_action_text_style(self):
        """ Test for type for API Field

        action_badge.text_style field must be str
        """

        assert type(self.api_data['action_badge']['text_style']) is str


    def test_api_field_exists_action_badge_url(self):
        """ Test for existance of API Field

        action_badge.url field must exist
        """

        assert 'url' in self.api_data['action_badge']


    def test_api_field_type_action_url(self):
        """ Test for type for API Field

        action_badge.url field must be str
        """

        assert type(self.api_data['action_badge']['url']) is str



    def test_api_field_exists_category(self):
        """ Test for existance of API Field

        category field must exist
        """

        assert 'category' in self.api_data


    def test_api_field_type_category(self):
        """ Test for type for API Field

        category field must be dict
        """

        assert type(self.api_data['category']) is dict


    def test_api_field_exists_category_id(self):
        """ Test for existance of API Field

        category.id field must exist
        """

        assert 'id' in self.api_data['category']


    def test_api_field_type_category_id(self):
        """ Test for type for API Field

        category.id field must be int
        """

        assert type(self.api_data['category']['id']) is int


    def test_api_field_exists_category_display_name(self):
        """ Test for existance of API Field

        category.display_name field must exist
        """

        assert 'display_name' in self.api_data['category']


    def test_api_field_type_category_display_name(self):
        """ Test for type for API Field

        category.display_name field must be str
        """

        assert type(self.api_data['category']['display_name']) is str


    def test_api_field_exists_category_url(self):
        """ Test for existance of API Field

        category.url field must exist
        """

        assert 'url' in self.api_data['category']


    def test_api_field_type_category_url(self):
        """ Test for type for API Field

        category.url field must be Hyperlink
        """

        assert type(self.api_data['category']['url']) is Hyperlink



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



    def test_api_field_exists_software(self):
        """ Test for existance of API Field

        software field must exist
        """

        assert 'software' in self.api_data


    def test_api_field_type_software(self):
        """ Test for type for API Field

        software field must be dict
        """

        assert type(self.api_data['software']) is dict


    def test_api_field_exists_software_id(self):
        """ Test for existance of API Field

        software.id field must exist
        """

        assert 'id' in self.api_data['software']


    def test_api_field_type_software_id(self):
        """ Test for type for API Field

        software.id field must be int
        """

        assert type(self.api_data['software']['id']) is int


    def test_api_field_exists_software_display_name(self):
        """ Test for existance of API Field

        software.display_name field must exist
        """

        assert 'display_name' in self.api_data['software']


    def test_api_field_type_software_display_name(self):
        """ Test for type for API Field

        software.display_name field must be str
        """

        assert type(self.api_data['software']['display_name']) is str


    def test_api_field_exists_software_url(self):
        """ Test for existance of API Field

        software.url field must exist
        """

        assert 'url' in self.api_data['software']


    def test_api_field_type_software_url(self):
        """ Test for type for API Field

        software.url field must be Hyperlink
        """

        assert type(self.api_data['software']['url']) is Hyperlink



    def test_api_field_exists_category(self):
        """ Test for existance of API Field

        category field must exist
        """

        assert 'category' in self.api_data


    def test_api_field_type_category(self):
        """ Test for type for API Field

        category field must be dict
        """

        assert type(self.api_data['category']) is dict


    def test_api_field_exists_category_id(self):
        """ Test for existance of API Field

        category.id field must exist
        """

        assert 'id' in self.api_data['category']


    def test_api_field_type_category_id(self):
        """ Test for type for API Field

        category.id field must be int
        """

        assert type(self.api_data['category']['id']) is int


    def test_api_field_exists_category_display_name(self):
        """ Test for existance of API Field

        category.display_name field must exist
        """

        assert 'display_name' in self.api_data['category']


    def test_api_field_type_category_display_name(self):
        """ Test for type for API Field

        category.display_name field must be str
        """

        assert type(self.api_data['category']['display_name']) is str


    def test_api_field_exists_category_url(self):
        """ Test for existance of API Field

        category.url field must exist
        """

        assert 'url' in self.api_data['category']


    def test_api_field_type_category_url(self):
        """ Test for type for API Field

        category.url field must be Hyperlink
        """

        assert type(self.api_data['category']['url']) is Hyperlink



    def test_api_field_exists_version(self):
        """ Test for existance of API Field

        version field must exist
        """

        assert 'version' in self.api_data


    def test_api_field_type_version(self):
        """ Test for type for API Field

        version field must be dict
        """

        assert type(self.api_data['version']) is dict


    def test_api_field_exists_version_id(self):
        """ Test for existance of API Field

        version.id field must exist
        """

        assert 'id' in self.api_data['version']


    def test_api_field_type_version_id(self):
        """ Test for type for API Field

        version.id field must be int
        """

        assert type(self.api_data['version']['id']) is int


    def test_api_field_exists_version_display_name(self):
        """ Test for existance of API Field

        version.display_name field must exist
        """

        assert 'display_name' in self.api_data['version']


    def test_api_field_type_version_display_name(self):
        """ Test for type for API Field

        version.display_name field must be str
        """

        assert type(self.api_data['version']['display_name']) is str


    def test_api_field_exists_version_url(self):
        """ Test for existance of API Field

        version.url field must exist
        """

        assert 'url' in self.api_data['version']


    def test_api_field_type_version_url(self):
        """ Test for type for API Field

        version.url field must be str
        """

        assert type(self.api_data['version']['url']) is str



    def test_api_field_exists_installedversion(self):
        """ Test for existance of API Field

        installedversion field must exist
        """

        assert 'installedversion' in self.api_data


    def test_api_field_type_installedversion(self):
        """ Test for type for API Field

        installedversion field must be dict
        """

        assert type(self.api_data['installedversion']) is dict


    def test_api_field_exists_installedversion_id(self):
        """ Test for existance of API Field

        installedversion.id field must exist
        """

        assert 'id' in self.api_data['installedversion']


    def test_api_field_type_installedversion_id(self):
        """ Test for type for API Field

        installedversion.id field must be int
        """

        assert type(self.api_data['installedversion']['id']) is int


    def test_api_field_exists_installedversion_display_name(self):
        """ Test for existance of API Field

        installedversion.display_name field must exist
        """

        assert 'display_name' in self.api_data['installedversion']


    def test_api_field_type_installedversion_display_name(self):
        """ Test for type for API Field

        installedversion.display_name field must be str
        """

        assert type(self.api_data['installedversion']['display_name']) is str


    def test_api_field_exists_installedversion_url(self):
        """ Test for existance of API Field

        installedversion.url field must exist
        """

        assert 'url' in self.api_data['installedversion']


    def test_api_field_type_installedversion_url(self):
        """ Test for type for API Field

        installedversion.url field must be str
        """

        assert type(self.api_data['installedversion']['url']) is str
