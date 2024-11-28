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

from itam.models.device import Device, DeviceModel, DeviceType



class DeviceAPI(
    TestCase,
    APITenancyObject
):

    model = Device

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

        device_model = DeviceModel.objects.create(
            organization = self.organization,
            name = 'a model',
            manufacturer = manufacturer
        )

        device_type = DeviceType.objects.create(
            organization = self.organization,
            name = 'computer'
        )


        self.item = self.model.objects.create(
            organization = self.organization,
            name = 'one',
            config = dict({"key": "one", "existing": "dont_over_write"}),
            model_notes = 'a note',
            uuid = '00000000-0000-0000-0000-000000000000',
            serial_number = 'serial-number',
            device_model = device_model,
            device_type = device_type,
            inventorydate = '2024-01-01 01:01:00'
        )


        self.url_view_kwargs = {'pk': self.item.id}

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
        url = reverse('v2:_api_v2_device-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data = response.data



    def test_api_field_exists_config(self):
        """ Test for existance of API Field

        config field must exist
        """

        assert 'config' in self.api_data


    def test_api_field_type_config(self):
        """ Test for type for API Field

        config field must be dict
        """

        assert type(self.api_data['config']) is dict



    def test_api_field_exists_status_icon(self):
        """ Test for existance of API Field

        status_icon field must exist
        """

        assert 'status_icon' in self.api_data


    def test_api_field_type_status_icon(self):
        """ Test for type for API Field

        status_icon field must be list
        """

        assert type(self.api_data['status_icon']) is list



    def test_api_field_exists_serial_number(self):
        """ Test for existance of API Field

        serial_number field must exist
        """

        assert 'serial_number' in self.api_data


    def test_api_field_type_serial_number(self):
        """ Test for type for API Field

        serial_number field must be str
        """

        assert type(self.api_data['serial_number']) is str



    def test_api_field_exists_uuid(self):
        """ Test for existance of API Field

        uuid field must exist
        """

        assert 'uuid' in self.api_data


    def test_api_field_type_uuid(self):
        """ Test for type for API Field

        uuid field must be str
        """

        assert type(self.api_data['uuid']) is str



    def test_api_field_exists_is_virtual(self):
        """ Test for existance of API Field

        is_virtual field must exist
        """

        assert 'is_virtual' in self.api_data


    def test_api_field_type_is_virtual(self):
        """ Test for type for API Field

        is_virtual field must be bool
        """

        assert type(self.api_data['is_virtual']) is bool



    def test_api_field_exists_inventorydate(self):
        """ Test for existance of API Field

        inventorydate field must exist
        """

        assert 'inventorydate' in self.api_data


    def test_api_field_type_inventorydate(self):
        """ Test for type for API Field

        inventorydate field must be str
        """

        assert type(self.api_data['inventorydate']) is str



    def test_api_field_exists_device_type(self):
        """ Test for existance of API Field

        device_type field must exist
        """

        assert 'device_type' in self.api_data


    def test_api_field_type_device_type(self):
        """ Test for type for API Field

        device_type field must be dict
        """

        assert type(self.api_data['device_type']) is dict


    def test_api_field_exists_device_type_id(self):
        """ Test for existance of API Field

        device_type.id field must exist
        """

        assert 'id' in self.api_data['device_type']


    def test_api_field_type_device_type_id(self):
        """ Test for type for API Field

        device_type.id field must be int
        """

        assert type(self.api_data['device_type']['id']) is int


    def test_api_field_exists_device_type_display_name(self):
        """ Test for existance of API Field

        device_type.display_name field must exist
        """

        assert 'display_name' in self.api_data['device_type']


    def test_api_field_type_device_type_display_name(self):
        """ Test for type for API Field

        device_type.display_name field must be str
        """

        assert type(self.api_data['device_type']['display_name']) is str


    def test_api_field_exists_device_type_url(self):
        """ Test for existance of API Field

        device_type.url field must exist
        """

        assert 'url' in self.api_data['device_type']


    def test_api_field_type_device_type_url(self):
        """ Test for type for API Field

        device_type.url field must be Hyperlink
        """

        assert type(self.api_data['device_type']['url']) is Hyperlink



    def test_api_field_exists_device_model(self):
        """ Test for existance of API Field

        device_model field must exist
        """

        assert 'device_model' in self.api_data


    def test_api_field_type_device_model(self):
        """ Test for type for API Field

        device_model field must be dict
        """

        assert type(self.api_data['device_model']) is dict


    def test_api_field_exists_device_model_id(self):
        """ Test for existance of API Field

        device_model.id field must exist
        """

        assert 'id' in self.api_data['device_model']


    def test_api_field_type_device_model_id(self):
        """ Test for type for API Field

        device_model.id field must be int
        """

        assert type(self.api_data['device_model']['id']) is int


    def test_api_field_exists_device_model_display_name(self):
        """ Test for existance of API Field

        device_model.display_name field must exist
        """

        assert 'display_name' in self.api_data['device_model']


    def test_api_field_type_device_model_display_name(self):
        """ Test for type for API Field

        device_model.display_name field must be str
        """

        assert type(self.api_data['device_model']['display_name']) is str


    def test_api_field_exists_device_model_url(self):
        """ Test for existance of API Field

        device_model.url field must exist
        """

        assert 'url' in self.api_data['device_model']


    def test_api_field_type_device_model_url(self):
        """ Test for type for API Field

        device_model.url field must be Hyperlink
        """

        assert type(self.api_data['device_model']['url']) is Hyperlink



    def test_api_field_exists_organization(self):
        """ Test for existance of API Field

        organization field must exist
        """

        assert 'organization' in self.api_data


    def test_api_field_type_organization(self):
        """ Test for type for API Field

        organization field must be dict
        """

        assert type(self.api_data['organization']) is dict


    def test_api_field_exists_organization_id(self):
        """ Test for existance of API Field

        organization.id field must exist
        """

        assert 'id' in self.api_data['organization']


    def test_api_field_type_organization_id(self):
        """ Test for type for API Field

        organization.id field must be int
        """

        assert type(self.api_data['organization']['id']) is int


    def test_api_field_exists_organization_display_name(self):
        """ Test for existance of API Field

        organization.display_name field must exist
        """

        assert 'display_name' in self.api_data['organization']


    def test_api_field_type_organization_display_name(self):
        """ Test for type for API Field

        organization.display_name field must be str
        """

        assert type(self.api_data['organization']['display_name']) is str


    def test_api_field_exists_organization_url(self):
        """ Test for existance of API Field

        organization.url field must exist
        """

        assert 'url' in self.api_data['organization']


    def test_api_field_type_organization_url(self):
        """ Test for type for API Field

        organization.url field must be Hyperlink
        """

        assert type(self.api_data['organization']['url']) is Hyperlink



    def test_api_field_exists_urls_device_model(self):
        """ Test for existance of API Field

        _urls.device_model field must exist
        """

        assert 'device_model' in self.api_data['_urls']


    def test_api_field_type_urls_device_model(self):
        """ Test for type for API Field

        _urls.device_model field must be str
        """

        assert type(self.api_data['_urls']['device_model']) is str



    def test_api_field_exists_urls_device_type(self):
        """ Test for existance of API Field

        _urls.device_type field must exist
        """

        assert 'device_type' in self.api_data['_urls']


    def test_api_field_type_urls_device_type(self):
        """ Test for type for API Field

        _urls.device_type field must be str
        """

        assert type(self.api_data['_urls']['device_type']) is str



    def test_api_field_exists_urls_external_links(self):
        """ Test for existance of API Field

        _urls.external_links field must exist
        """

        assert 'external_links' in self.api_data['_urls']


    def test_api_field_type_urls_external_links(self):
        """ Test for type for API Field

        _urls.external_links field must be str
        """

        assert type(self.api_data['_urls']['external_links']) is str



    def test_api_field_exists_urls_history(self):
        """ Test for existance of API Field

        _urls.history field must exist
        """

        assert 'history' in self.api_data['_urls']


    def test_api_field_type_urls_history(self):
        """ Test for type for API Field

        _urls.history field must be str
        """

        assert type(self.api_data['_urls']['history']) is str



    def test_api_field_exists_urls_notes(self):
        """ Test for existance of API Field

        _urls.notes field must exist
        """

        assert 'notes' in self.api_data['_urls']


    def test_api_field_type_urls_notes(self):
        """ Test for type for API Field

        _urls.notes field must be str
        """

        assert type(self.api_data['_urls']['notes']) is str



    def test_api_field_exists_urls_service(self):
        """ Test for existance of API Field

        _urls.service field must exist
        """

        assert 'service' in self.api_data['_urls']


    def test_api_field_type_urls_service(self):
        """ Test for type for API Field

        _urls.service field must be str
        """

        assert type(self.api_data['_urls']['service']) is str



    def test_api_field_exists_urls_software(self):
        """ Test for existance of API Field

        _urls.software field must exist
        """

        assert 'software' in self.api_data['_urls']


    def test_api_field_type_urls_software(self):
        """ Test for type for API Field

        _urls.software field must be str
        """

        assert type(self.api_data['_urls']['software']) is str



    def test_api_field_exists_urls_tickets(self):
        """ Test for existance of API Field

        _urls.tickets field must exist
        """

        assert 'tickets' in self.api_data['_urls']


    def test_api_field_type_urls_tickets(self):
        """ Test for type for API Field

        _urls.tickets field must be str
        """

        assert type(self.api_data['_urls']['tickets']) is str
