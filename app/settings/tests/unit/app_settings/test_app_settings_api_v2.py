import pytest
import unittest

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from rest_framework.relations import Hyperlink

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_fields import APICommonFields

from settings.models.app_settings import AppSettings
from settings.models.user_settings import UserSettings



class AppSettingsAPI(
    TestCase,
    APICommonFields
):

    model = AppSettings

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create an item

        """

        self.organization = Organization.objects.create(name='test_org')

        self.item = AppSettings.objects.get( id = 1 )

        self.item.global_organization = self.organization

        self.item.save()


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

        user_settings = UserSettings.objects.get(user =  self.view_user)
        
        user_settings.default_organization = self.organization

        user_settings.save()


        teamuser = TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )


        self.url_view_kwargs = {'pk': self.item.id}

        client = Client()
        url = reverse('API:_api_v2_app_settings-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data = response.data



    def test_api_field_exists_device_model_is_global(self):
        """ Test for existance of API Field

        device_model_is_global field must exist
        """

        assert 'device_model_is_global' in self.api_data


    def test_api_field_type_device_model_is_global(self):
        """ Test for type for API Field

        device_model_is_global field must be bool
        """

        assert type(self.api_data['device_model_is_global']) is bool



    def test_api_field_exists_device_type_is_global(self):
        """ Test for existance of API Field

        device_type_is_global field must exist
        """

        assert 'device_type_is_global' in self.api_data


    def test_api_field_type_device_type_is_global(self):
        """ Test for type for API Field

        device_type_is_global field must be bool
        """

        assert type(self.api_data['device_type_is_global']) is bool



    def test_api_field_exists_manufacturer_is_global(self):
        """ Test for existance of API Field

        manufacturer_is_global field must exist
        """

        assert 'manufacturer_is_global' in self.api_data


    def test_api_field_type_manufacturer_is_global(self):
        """ Test for type for API Field

        manufacturer_is_global field must be bool
        """

        assert type(self.api_data['manufacturer_is_global']) is bool



    def test_api_field_exists_software_is_global(self):
        """ Test for existance of API Field

        software_is_global field must exist
        """

        assert 'software_is_global' in self.api_data


    def test_api_field_type_software_is_global(self):
        """ Test for type for API Field

        software_is_global field must be bool
        """

        assert type(self.api_data['software_is_global']) is bool



    def test_api_field_exists_software_categories_is_global(self):
        """ Test for existance of API Field

        software_categories_is_global field must exist
        """

        assert 'software_categories_is_global' in self.api_data


    def test_api_field_type_software_categories_is_global(self):
        """ Test for type for API Field

        software_categories_is_global field must be bool
        """

        assert type(self.api_data['software_categories_is_global']) is bool



    def test_api_field_exists_global_organization(self):
        """ Test for existance of API Field

        global_organization field must exist
        """

        assert 'global_organization' in self.api_data


    def test_api_field_type_global_organization(self):
        """ Test for type for API Field

        global_organization field must be dict
        """

        assert type(self.api_data['global_organization']) is dict


    def test_api_field_exists_global_organization_id(self):
        """ Test for existance of API Field

        global_organization.id field must exist
        """

        assert 'id' in self.api_data['global_organization']


    def test_api_field_type_global_organization_id(self):
        """ Test for type for API Field

        global_organization.id field must be dict
        """

        assert type(self.api_data['global_organization']['id']) is int


    def test_api_field_exists_global_organization_display_name(self):
        """ Test for existance of API Field

        global_organization.display_name field must exist
        """

        assert 'display_name' in self.api_data['global_organization']


    def test_api_field_type_global_organization_display_name(self):
        """ Test for type for API Field

        global_organization.display_name field must be str
        """

        assert type(self.api_data['global_organization']['display_name']) is str


    def test_api_field_exists_global_organization_url(self):
        """ Test for existance of API Field

        global_organization.url field must exist
        """

        assert 'url' in self.api_data['global_organization']


    def test_api_field_type_global_organization_url(self):
        """ Test for type for API Field

        global_organization.url field must be str
        """

        assert type(self.api_data['global_organization']['url']) is Hyperlink
