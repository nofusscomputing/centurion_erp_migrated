import pytest
import unittest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from rest_framework.relations import Hyperlink

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_fields import APICommonFields


class OrganizationAPI(
    TestCase,
    APICommonFields
):

    model = Organization

    app_namespace = 'v2'
    
    url_name = '_api_v2_organization'

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create the object
        2. create view user
        3. add user as org manager
        4. make api request
        """

        organization = Organization.objects.create(name='test_org', model_notes='random text')

        self.organization = organization


        self.item = organization

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
            organization = organization,
        )

        view_team.permissions.set([view_permissions])


        self.view_user = User.objects.create_user(username="test_user_view", password="password")
        teamuser = TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )

        organization.manager = self.view_user

        organization.save()


        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


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



    def test_api_field_exists_manager(self):
        """ Test for existance of API Field

        manager field must exist
        """

        assert 'manager' in self.api_data


    def test_api_field_type_manager(self):
        """ Test for type for API Field

        manager field must be dict
        """

        assert type(self.api_data['manager']) is dict


    def test_api_field_exists_manager_id(self):
        """ Test for existance of API Field

        manager.id field must exist
        """

        assert 'id' in self.api_data['manager']


    def test_api_field_type_manager_id(self):
        """ Test for type for API Field

        manager.id field must be int
        """

        assert type(self.api_data['manager']['id']) is int


    def test_api_field_exists_manager_display_name(self):
        """ Test for existance of API Field

        manager.display_name field must exist
        """

        assert 'display_name' in self.api_data['manager']


    def test_api_field_type_manager_display_name(self):
        """ Test for type for API Field

        manager.display_name field must be int
        """

        assert type(self.api_data['manager']['display_name']) is str


    def test_api_field_exists_manager_url(self):
        """ Test for existance of API Field

        manager.display_name field must exist
        """

        assert 'url' in self.api_data['manager']


    def test_api_field_type_manager_url(self):
        """ Test for type for API Field

        manager.url field must be Hyperlink
        """

        assert type(self.api_data['manager']['url']) is Hyperlink



    def test_api_field_exists_url_teams(self):
        """ Test for existance of API Field

        _urls.teams field must exist
        """

        assert 'teams' in self.api_data['_urls']


    def test_api_field_type_url_teams(self):
        """ Test for type for API Field

        _urls.teams field must be Hyperlink
        """

        assert type(self.api_data['_urls']['teams']) is str
