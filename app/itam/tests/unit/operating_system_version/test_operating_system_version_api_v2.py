import pytest
import unittest

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from rest_framework.relations import Hyperlink

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_fields import APITenancyObject

from itam.models.operating_system import OperatingSystem, OperatingSystemVersion



class OperatingSystemVersionAPI(
    TestCase,
    APITenancyObject
):

    model = OperatingSystemVersion

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create an item

        """

        self.organization = Organization.objects.create(name='test_org')

        operating_system = OperatingSystem.objects.create(
            organization = self.organization,
            name = 'one',
            model_notes = 'a note'
        )

        self.item = self.model.objects.create(
            organization = self.organization,
            name = '10',
            model_notes = 'a note',
            operating_system = operating_system
        )


        self.url_view_kwargs = {'operating_system_id': operating_system.id, 'pk': self.item.id}

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
        url = reverse('API:_api_v2_operating_system_version-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data = response.data


    def test_api_field_exists_operating_system(self):
        """ Test for existance of API Field

        operating_system field must exist
        """

        assert 'operating_system' in self.api_data


    def test_api_field_type_operating_system(self):
        """ Test for type for API Field

        operating_system field must be dict
        """

        assert type(self.api_data['operating_system']) is dict


    def test_api_field_exists_operating_system_id(self):
        """ Test for existance of API Field

        operating_system.id field must exist
        """

        assert 'id' in self.api_data['operating_system']


    def test_api_field_type_operating_system_id(self):
        """ Test for type for API Field

        operating_system.id field must be int
        """

        assert type(self.api_data['operating_system']['id']) is int


    def test_api_field_exists_operating_system_display_name(self):
        """ Test for existance of API Field

        operating_system.display_name field must exist
        """

        assert 'display_name' in self.api_data['operating_system']


    def test_api_field_type_operating_system_display_name(self):
        """ Test for type for API Field

        operating_system.display_name field must be str
        """

        assert type(self.api_data['operating_system']['display_name']) is str


    def test_api_field_exists_operating_system_url(self):
        """ Test for existance of API Field

        operating_system.url field must exist
        """

        assert 'url' in self.api_data['operating_system']


    def test_api_field_type_operating_system_url(self):
        """ Test for type for API Field

        operating_system.url field must be Hyperlink
        """

        assert type(self.api_data['operating_system']['url']) is Hyperlink

