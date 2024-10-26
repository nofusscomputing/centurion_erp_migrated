import pytest
import unittest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from rest_framework.relations import Hyperlink

from access.models import Organization, Team, TeamUsers, Permission



class OrganizationAPI(TestCase):

    model = Organization

    app_namespace = 'v1'
    
    url_name = '_api_organization'

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

        different_organization = Organization.objects.create(name='test_different_organization')


        self.item = organization

        self.url_view_kwargs = {'pk': self.item.id}

        self.url_kwargs = {'pk': self.item.id}

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


        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name, kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data = response.data



    def test_api_field_exists_id(self):
        """ Test for existance of API Field

        id field must exist
        """

        assert 'id' in self.api_data


    def test_api_field_type_id(self):
        """ Test for type for API Field

        id field must be int
        """

        assert type(self.api_data['id']) is int


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


    def test_api_field_exists_teams(self):
        """ Test for existance of API Field

        teams field must exist
        """

        assert 'teams' in self.api_data


    def test_api_field_type_teams(self):
        """ Test for type for API Field

        teams field must be list
        """

        assert type(self.api_data['teams']) is list


    def test_api_field_exists_url(self):
        """ Test for existance of API Field

        url field must exist
        """

        assert 'url' in self.api_data


    def test_api_field_type_url(self):
        """ Test for type for API Field

        url field must be str
        """

        assert type(self.api_data['url']) is Hyperlink




    def test_api_field_exists_teams_id(self):
        """ Test for existance of API Field

        teams.id field must exist
        """

        assert 'id' in self.api_data['teams'][0]


    def test_api_field_type_teams_id(self):
        """ Test for type for API Field

        teams.id field must be int
        """

        assert type(self.api_data['teams'][0]['id']) is int


    def test_api_field_exists_teams_team_name(self):
        """ Test for existance of API Field

        teams.team_name field must exist
        """

        assert 'team_name' in self.api_data['teams'][0]


    def test_api_field_type_teams_team_name(self):
        """ Test for type for API Field

        teams.team_name field must be string
        """

        assert type(self.api_data['teams'][0]['team_name']) is str


    def test_api_field_exists_teams_permissions(self):
        """ Test for existance of API Field

        teams.permissions field must exist
        """

        assert 'permissions' in self.api_data['teams'][0]


    def test_api_field_type_teams_permissions(self):
        """ Test for type for API Field

        teams.permissions field must be list
        """

        assert type(self.api_data['teams'][0]['permissions']) is list


    def test_api_field_exists_teams_permissions_url(self):
        """ Test for existance of API Field

        teams.permissions_url field must exist
        """

        assert 'permissions_url' in self.api_data['teams'][0]


    def test_api_field_type_teams_permissions_url(self):
        """ Test for type for API Field

        teams.permissions_url field must be url
        """

        assert type(self.api_data['teams'][0]['permissions_url']) is str


    def test_api_field_exists_teams_url(self):
        """ Test for existance of API Field

        teams.url field must exist
        """

        assert 'url' in self.api_data['teams'][0]


    def test_api_field_type_teams_url(self):
        """ Test for type for API Field

        teams.url field must be url
        """

        assert type(self.api_data['teams'][0]['url']) is str



    def test_api_field_exists_teams_permissions_id(self):
        """ Test for existance of API Field

        teams.permissions.id field must exist
        """

        assert 'id' in self.api_data['teams'][0]['permissions'][0]


    def test_api_field_type_teams_permissions_id(self):
        """ Test for type for API Field

        teams.permissions.id field must be int
        """

        assert type(self.api_data['teams'][0]['permissions'][0]['id']) is int


    def test_api_field_exists_teams_permissions_name(self):
        """ Test for existance of API Field

        teams.permissions.name field must exist
        """

        assert 'name' in self.api_data['teams'][0]['permissions'][0]


    def test_api_field_type_teams_permissions_name(self):
        """ Test for type for API Field

        teams.permissions.name field must be str
        """

        assert type(self.api_data['teams'][0]['permissions'][0]['name']) is str


    def test_api_field_exists_teams_permissions_codename(self):
        """ Test for existance of API Field

        teams.permissions.codename field must exist
        """

        assert 'codename' in self.api_data['teams'][0]['permissions'][0]


    def test_api_field_type_teams_permissions_codename(self):
        """ Test for type for API Field

        teams.permissions.codename field must be str
        """

        assert type(self.api_data['teams'][0]['permissions'][0]['codename']) is str


    def test_api_field_exists_teams_permissions_content_type(self):
        """ Test for existance of API Field

        teams.permissions.content_type field must exist
        """

        assert 'content_type' in self.api_data['teams'][0]['permissions'][0]


    def test_api_field_type_teams_permissions_content_type(self):
        """ Test for type for API Field

        teams.permissions.content_type field must be dict
        """

        assert type(self.api_data['teams'][0]['permissions'][0]['content_type']) is dict



    def test_api_field_exists_teams_permissions_content_type_id(self):
        """ Test for existance of API Field

        teams.permissions.content_type.id field must exist
        """

        assert 'id' in self.api_data['teams'][0]['permissions'][0]['content_type']


    def test_api_field_type_teams_permissions_content_type_id(self):
        """ Test for type for API Field

        teams.permissions.content_type.id field must be int
        """

        assert type(self.api_data['teams'][0]['permissions'][0]['content_type']['id']) is int


    def test_api_field_exists_teams_permissions_content_type_app_label(self):
        """ Test for existance of API Field

        teams.permissions.content_type.app_label field must exist
        """

        assert 'app_label' in self.api_data['teams'][0]['permissions'][0]['content_type']


    def test_api_field_type_teams_permissions_content_type_app_label(self):
        """ Test for type for API Field

        teams.permissions.content_type.app_label field must be str
        """

        assert type(self.api_data['teams'][0]['permissions'][0]['content_type']['app_label']) is str


    def test_api_field_exists_teams_permissions_content_type_model(self):
        """ Test for existance of API Field

        teams.permissions.content_type.model field must exist
        """

        assert 'model' in self.api_data['teams'][0]['permissions'][0]['content_type']


    def test_api_field_type_teams_permissions_content_type_model(self):
        """ Test for type for API Field

        teams.permissions.content_type.model field must be str
        """

        assert type(self.api_data['teams'][0]['permissions'][0]['content_type']['model']) is str
