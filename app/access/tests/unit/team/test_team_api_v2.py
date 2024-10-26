import pytest

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from rest_framework.relations import Hyperlink

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_fields import APITenancyObject



class TeamAPI(
    TestCase,
    APITenancyObject
):

    model = Team

    app_namespace = 'v2'
    
    url_name = '_api_v2_organization_team'

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create the object
        2. create view user
        3. add user as org manager
        4. make api request
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        different_organization = Organization.objects.create(name='test_different_organization')


        self.item = self.model.objects.create(
            organization=organization,
            team_name = 'teamone',
            model_notes = 'random note'
        )

        self.url_view_kwargs = {'organization_id': self.organization.id, 'pk': self.item.id}

        view_permissions = Permission.objects.get(
                codename = 'view_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        self.item.permissions.set([view_permissions])

        self.view_user = User.objects.create_user(username="test_user_view", password="password")
        teamuser = TeamUsers.objects.create(
            team = self.item,
            user = self.view_user
        )

        organization.manager = self.view_user

        organization.save()

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data = response.data




    def test_api_field_exists_team_name(self):
        """ Test for existance of API Field

        team_name field must exist
        """

        assert 'team_name' in self.api_data


    def test_api_field_type_team_name(self):
        """ Test for type for API Field

        team_name field must be str
        """

        assert type(self.api_data['team_name']) is str



    def test_api_field_exists_permissions(self):
        """ Test for existance of API Field

        permissions field must exist
        """

        assert 'permissions' in self.api_data


    def test_api_field_type_permissions(self):
        """ Test for type for API Field

        url field must be list
        """

        assert type(self.api_data['permissions']) is list



    def test_api_field_exists_permissions_id(self):
        """ Test for existance of API Field

        permissions.id field must exist
        """

        assert 'id' in self.api_data['permissions'][0]


    def test_api_field_type_permissions_id(self):
        """ Test for type for API Field

        permissions.id field must be int
        """

        assert type(self.api_data['permissions'][0]['id']) is int


    def test_api_field_exists_permissions_display_name(self):
        """ Test for existance of API Field

        permissions.display_name field must exist
        """

        assert 'display_name' in self.api_data['permissions'][0]


    def test_api_field_type_permissions_display_name(self):
        """ Test for type for API Field

        permissions.display_name field must be str
        """

        assert type(self.api_data['permissions'][0]['display_name']) is str



    def test_api_field_exists_permissions_url(self):
        """ Test for existance of API Field

        permissions.url field must exist
        """

        assert 'url' in self.api_data['permissions'][0]


    def test_api_field_type_permissions_url(self):
        """ Test for type for API Field

        permissions.url field must be str
        """

        assert type(self.api_data['permissions'][0]['url']) is Hyperlink
