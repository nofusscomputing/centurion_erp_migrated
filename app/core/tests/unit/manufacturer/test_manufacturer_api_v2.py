import pytest
import unittest

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_fields import APITenancyObject

from core.models.manufacturer import Manufacturer



class ManufacturerAPI(
    TestCase,
    APITenancyObject
):

    model = Manufacturer

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create an item

        """

        self.organization = Organization.objects.create(name='test_org')


        self.item = self.model.objects.create(
            organization = self.organization,
            name = 'one',
            model_notes = 'text'
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
        url = reverse('API:_api_v2_manufacturer-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data = response.data



    def test_api_field_exists_name(self):
        """ Test for existance of API Field

        name field must exist
        """

        assert 'name' in self.api_data


    def test_api_field_type_name(self):
        """ Test for type for API Field

        name field must be str
        """

        assert type(self.api_data['name']) is str



    def test_api_field_exists_url_history(self):
        """ Test for existance of API Field

        _urls.history field must exist
        """

        assert 'history' in self.api_data['_urls']


    def test_api_field_type_url_history(self):
        """ Test for type for API Field

        _urls.history field must be str
        """

        assert type(self.api_data['_urls']['history']) is str
