import pytest
import unittest

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from rest_framework.relations import Hyperlink

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_fields import APITenancyObject

from assistance.models.knowledge_base import KnowledgeBase

from project_management.models.project_types import ProjectType

from settings.models.user_settings import UserSettings



class ProjectTypeAPI(
    TestCase,
    APITenancyObject
):

    model = ProjectType

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create an item

        """

        self.organization = Organization.objects.create(name='test_org')


        kb = KnowledgeBase.objects.create(
            organization = self.organization,
            title = 'kb article'
        )

        self.item = self.model.objects.create(
            organization = self.organization,
            name = 'a state',
            model_notes = 'note',
            runbook = kb,
        )


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
        url = reverse('API:_api_v2_project_type-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data = response.data



    def test_api_field_exists_runbook(self):
        """ Test for existance of API Field

        runbook field must exist
        """

        assert 'runbook' in self.api_data


    def test_api_field_type_runbook(self):
        """ Test for type for API Field

        runbook field must be dict
        """

        assert type(self.api_data['runbook']) is dict



    def test_api_field_exists_runbook_id(self):
        """ Test for existance of API Field

        runbook.id field must exist
        """

        assert 'id' in self.api_data['runbook']


    def test_api_field_type_runbook_id(self):
        """ Test for type for API Field

        runbook.id field must be int
        """

        assert type(self.api_data['runbook']['id']) is int


    def test_api_field_exists_runbook_display_name(self):
        """ Test for existance of API Field

        runbook.display_name field must exist
        """

        assert 'display_name' in self.api_data['runbook']


    def test_api_field_type_runbook_display_name(self):
        """ Test for type for API Field

        runbook.display_name field must be str
        """

        assert type(self.api_data['runbook']['display_name']) is str


    def test_api_field_exists_runbook_url(self):
        """ Test for existance of API Field

        runbook.url field must exist
        """

        assert 'url' in self.api_data['runbook']


    def test_api_field_type_runbook_url(self):
        """ Test for type for API Field

        runbook.url field must be str
        """

        assert type(self.api_data['runbook']['url']) is str
