import pytest
import unittest

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from rest_framework.relations import Hyperlink

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_fields import APITenancyObject

from settings.models.external_link import ExternalLink
from settings.models.user_settings import UserSettings



class ExternalLinkAPI(
    TestCase,
    APITenancyObject
):

    model = ExternalLink

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create an item

        """

        self.organization = Organization.objects.create(name='test_org')


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

        self.item = self.model.objects.create(
            organization=self.organization,
            name = 'state',
            button_text = 'text',
            model_notes = 'sakjdhjak',
            template = 'boo',
            colour = '#fff'
        )

        self.url_view_kwargs = {'pk': self.item.id}

        client = Client()
        url = reverse('v2:_api_v2_external_link-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data = response.data



    def test_api_field_exists_button_text(self):
        """ Test for existance of API Field

        button_text field must exist
        """

        assert 'button_text' in self.api_data



    def test_api_field_type_button_text(self):
        """ Test for type for API Field

        button_text field must be str
        """

        assert type(self.api_data['button_text']) is str



    def test_api_field_exists_template(self):
        """ Test for existance of API Field

        template field must exist
        """

        assert 'template' in self.api_data



    def test_api_field_type_template(self):
        """ Test for type for API Field

        template field must be str
        """

        assert type(self.api_data['template']) is str



    def test_api_field_exists_colour(self):
        """ Test for existance of API Field

        colour field must exist
        """

        assert 'colour' in self.api_data



    def test_api_field_type_colour(self):
        """ Test for type for API Field

        colour field must be str
        """

        assert type(self.api_data['colour']) is str
