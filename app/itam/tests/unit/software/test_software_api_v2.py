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

from itam.models.software import Software, SoftwareCategory



class SoftwareAPI(
    TestCase,
    APITenancyObject
):

    model = Software

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


        self.item = self.model.objects.create(
            organization = self.organization,
            name = 'one',
            publisher = manufacturer,
            category = category,
            model_notes = 'a note'
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
        url = reverse('API:_api_v2_software-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data = response.data


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



    def test_api_field_exists_publisher(self):
        """ Test for existance of API Field

        publisher field must exist
        """

        assert 'publisher' in self.api_data


    def test_api_field_type_publisher(self):
        """ Test for type for API Field

        publisher field must be dict
        """

        assert type(self.api_data['publisher']) is dict


    def test_api_field_exists_publisher_id(self):
        """ Test for existance of API Field

        publisher.id field must exist
        """

        assert 'id' in self.api_data['publisher']


    def test_api_field_type_publisher_id(self):
        """ Test for type for API Field

        publisher.id field must be int
        """

        assert type(self.api_data['publisher']['id']) is int


    def test_api_field_exists_publisher_display_name(self):
        """ Test for existance of API Field

        publisher.display_name field must exist
        """

        assert 'display_name' in self.api_data['publisher']


    def test_api_field_type_publisher_display_name(self):
        """ Test for type for API Field

        publisher.display_name field must be str
        """

        assert type(self.api_data['publisher']['display_name']) is str


    def test_api_field_exists_publisher_url(self):
        """ Test for existance of API Field

        publisher.url field must exist
        """

        assert 'url' in self.api_data['publisher']


    def test_api_field_type_publisher_url(self):
        """ Test for type for API Field

        publisher.url field must be Hyperlink
        """

        assert type(self.api_data['publisher']['url']) is Hyperlink



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



    def test_api_field_exists_urls_version(self):
        """ Test for existance of API Field

        _urls.version field must exist
        """

        assert 'version' in self.api_data['_urls']


    def test_api_field_type_urls_notes(self):
        """ Test for type for API Field

        _urls.version field must be str
        """

        assert type(self.api_data['_urls']['version']) is str
