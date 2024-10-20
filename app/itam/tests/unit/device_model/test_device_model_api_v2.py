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

from itam.models.device import DeviceModel



class DeviceModelAPI(
    TestCase,
    APITenancyObject
):

    model = DeviceModel

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

        self.item = self.model.objects.create(
            organization = self.organization,
            name = 'a model',
            manufacturer = manufacturer,
            model_notes = 'a note',
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
        url = reverse('API:_api_v2_device_model-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data = response.data



    def test_api_field_exists_manufacturer(self):
        """ Test for existance of API Field

        manufacturer field must exist
        """

        assert 'manufacturer' in self.api_data


    def test_api_field_type_manufacturer(self):
        """ Test for type for API Field

        manufacturer field must be dict
        """

        assert type(self.api_data['manufacturer']) is dict


    def test_api_field_exists_manufacturer_id(self):
        """ Test for existance of API Field

        manufacturer.id field must exist
        """

        assert 'id' in self.api_data['manufacturer']


    def test_api_field_type_manufacturer_id(self):
        """ Test for type for API Field

        manufacturer.id field must be int
        """

        assert type(self.api_data['manufacturer']['id']) is int


    def test_api_field_exists_manufacturer_display_name(self):
        """ Test for existance of API Field

        manufacturer.display_name field must exist
        """

        assert 'display_name' in self.api_data['manufacturer']


    def test_api_field_type_manufacturer_display_name(self):
        """ Test for type for API Field

        manufacturer.display_name field must be str
        """

        assert type(self.api_data['manufacturer']['display_name']) is str


    def test_api_field_exists_manufacturer_url(self):
        """ Test for existance of API Field

        manufacturer.url field must exist
        """

        assert 'url' in self.api_data['manufacturer']


    def test_api_field_type_manufacturer_url(self):
        """ Test for type for API Field

        manufacturer.url field must be Hyperlink
        """

        assert type(self.api_data['manufacturer']['url']) is Hyperlink

