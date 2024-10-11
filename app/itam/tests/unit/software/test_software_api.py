import pytest
import unittest
import requests

from django.contrib.auth.models import AnonymousUser, User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from rest_framework.relations import Hyperlink

from access.models import Organization, Team, TeamUsers, Permission

from core.models.manufacturer import Manufacturer

from itam.models.software import Software, SoftwareCategory


class SoftwareAPI(TestCase):


    model = Software

    app_namespace = 'API'
    
    url_name = 'software-detail'


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a software
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        different_organization = Organization.objects.create(name='test_different_organization')

        category = SoftwareCategory.objects.create(
            name='a category',
            organization = organization,
        )

        publisher = Manufacturer.objects.create(
            name='a manufacturer',
            organization = organization,
        )


        self.item = self.model.objects.create(
            organization=organization,
            name = 'softwareone',
            model_notes = 'random str',
            category = category,
            publisher = publisher
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


    def test_api_field_exists_is_global(self):
        """ Test for existance of API Field

        is_global field must exist
        """

        assert 'is_global' in self.api_data


    def test_api_field_type_is_global(self):
        """ Test for type for API Field

        is_global field must be boolean
        """

        assert type(self.api_data['is_global']) is bool


    def test_api_field_exists_model_notes(self):
        """ Test for existance of API Field

        model_notes field must exist
        """

        assert 'model_notes' in self.api_data


    def test_api_field_type_model_notes(self):
        """ Test for type for API Field

        model_notes field must be str
        """

        assert type(self.api_data['model_notes']) is str


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


    def test_api_field_exists_slug(self):
        """ Test for existance of API Field

        slug field must exist
        """

        assert 'slug' in self.api_data


    def test_api_field_type_slug(self):
        """ Test for type for API Field

        slug field must be str
        """

        assert type(self.api_data['slug']) is str


    def test_api_field_exists_created(self):
        """ Test for existance of API Field

        created field must exist
        """

        assert 'created' in self.api_data


    def test_api_field_type_created(self):
        """ Test for type for API Field

        created field must be str
        """

        assert type(self.api_data['created']) is str


    def test_api_field_exists_modified(self):
        """ Test for existance of API Field

        modified field must exist
        """

        assert 'modified' in self.api_data


    def test_api_field_type_modified(self):
        """ Test for type for API Field

        modified field must be str
        """

        assert type(self.api_data['modified']) is str


    def test_api_field_exists_organization(self):
        """ Test for existance of API Field

        organization field must exist
        """

        assert 'organization' in self.api_data


    def test_api_field_type_organization(self):
        """ Test for type for API Field

        organization field must be intt
        """

        assert type(self.api_data['organization']) is int


    def test_api_field_exists_publisher(self):
        """ Test for existance of API Field

        publisher field must exist
        """

        assert 'publisher' in self.api_data


    def test_api_field_type_publisher(self):
        """ Test for type for API Field

        publisher field must be int
        """

        assert type(self.api_data['publisher']) is int


    def test_api_field_exists_category(self):
        """ Test for existance of API Field

        category field must exist
        """

        assert 'category' in self.api_data


    def test_api_field_type_category(self):
        """ Test for type for API Field

        category field must be int
        """

        assert type(self.api_data['category']) is int

