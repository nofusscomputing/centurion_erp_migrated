import pytest
import unittest

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from rest_framework.relations import Hyperlink

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_fields import APITenancyObject

from project_management.models.project_milestone import Project, ProjectMilestone

from settings.models.user_settings import UserSettings



class ProjectMilestoneAPI(
    TestCase,
    APITenancyObject
):

    model = ProjectMilestone

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create an item

        """

        self.organization = Organization.objects.create(name='test_org')

        project = Project.objects.create(
            organization = self.organization,
            name = 'a state'
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


        self.item = self.model.objects.create(
            organization = self.organization,
            name = 'one',
            description = 'notes',
            project = project,
            start_date = '2024-01-01 00:01:00',
            finish_date = '2024-01-01 00:01:01',
        )


        self.url_view_kwargs = {'project_id': project.id, 'pk': self.item.id}

        client = Client()
        url = reverse('v2:_api_v2_project_milestone-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data = response.data



    def test_api_field_exists_model_notes(self):
        """ Test for existance of API Field

        This test is a custom test of a test case with the same name.
        this model does not have a model_notes_field

        model_notes field must exist
        """

        assert 'model_notes' not in self.api_data


    def test_api_field_type_model_notes(self):
        """ Test for type for API Field

        This test is a custom test of a test case with the same name.
        this model does not have a model_notes_field

        model_notes field must be str
        """

        assert True



    def test_api_field_exists_description(self):
        """ Test for existance of API Field

        model_notes field must exist
        """

        assert 'description' in self.api_data


    def test_api_field_type_description(self):
        """ Test for type for API Field

        description field must be str
        """

        assert type(self.api_data['description']) is str



    def test_api_field_exists_start_date(self):
        """ Test for existance of API Field

        start_date field must exist
        """

        assert 'start_date' in self.api_data


    def test_api_field_type_start_date(self):
        """ Test for type for API Field

        start_date field must be str
        """

        assert type(self.api_data['start_date']) is str



    def test_api_field_exists_finish_date(self):
        """ Test for existance of API Field

        finish_date field must exist
        """

        assert 'finish_date' in self.api_data


    def test_api_field_type_finish_date(self):
        """ Test for type for API Field

        finish_date field must be str
        """

        assert type(self.api_data['finish_date']) is str





    def test_api_field_exists_project(self):
        """ Test for existance of API Field

        project field must exist
        """

        assert 'project' in self.api_data


    def test_api_field_type_project(self):
        """ Test for type for API Field

        project field must be dict
        """

        assert type(self.api_data['project']) is dict


    def test_api_field_exists_project_id(self):
        """ Test for existance of API Field

        project.id field must exist
        """

        assert 'id' in self.api_data['project']


    def test_api_field_type_project_id(self):
        """ Test for type for API Field

        project.id field must be int
        """

        assert type(self.api_data['project']['id']) is int


    def test_api_field_exists_project_display_name(self):
        """ Test for existance of API Field

        project.display_name field must exist
        """

        assert 'display_name' in self.api_data['project']


    def test_api_field_type_project_display_name(self):
        """ Test for type for API Field

        project.display_name field must be str
        """

        assert type(self.api_data['project']['display_name']) is str


    def test_api_field_exists_project_url(self):
        """ Test for existance of API Field

        project.url field must exist
        """

        assert 'url' in self.api_data['project']


    def test_api_field_type_project_url(self):
        """ Test for type for API Field

        project.url field must be Hyperlink
        """

        assert type(self.api_data['project']['url']) is Hyperlink








    # def test_api_field_exists_state(self):
    #     """ Test for existance of API Field

    #     state field must exist
    #     """

    #     assert 'state' in self.api_data


    # def test_api_field_type_state(self):
    #     """ Test for type for API Field

    #     state field must be dict
    #     """

    #     assert type(self.api_data['state']) is dict


    # def test_api_field_exists_state_id(self):
    #     """ Test for existance of API Field

    #     state.id field must exist
    #     """

    #     assert 'id' in self.api_data['state']


    # def test_api_field_type_state_id(self):
    #     """ Test for type for API Field

    #     state.id field must be int
    #     """

    #     assert type(self.api_data['state']['id']) is int


    # def test_api_field_exists_state_display_name(self):
    #     """ Test for existance of API Field

    #     state.display_name field must exist
    #     """

    #     assert 'display_name' in self.api_data['state']


    # def test_api_field_type_state_display_name(self):
    #     """ Test for type for API Field

    #     state.display_name field must be str
    #     """

    #     assert type(self.api_data['state']['display_name']) is str


    # def test_api_field_exists_state_url(self):
    #     """ Test for existance of API Field

    #     state.url field must exist
    #     """

    #     assert 'url' in self.api_data['state']


    # def test_api_field_type_state_url(self):
    #     """ Test for type for API Field

    #     state.url field must be Hyperlink
    #     """

    #     assert type(self.api_data['state']['url']) is Hyperlink



    # def test_api_field_exists_manager_user(self):
    #     """ Test for existance of API Field

    #     manager_user field must exist
    #     """

    #     assert 'manager_user' in self.api_data


    # def test_api_field_type_manager_user(self):
    #     """ Test for type for API Field

    #     manager_user field must be dict
    #     """

    #     assert type(self.api_data['manager_user']) is dict


    # def test_api_field_exists_manager_user_id(self):
    #     """ Test for existance of API Field

    #     manager_user.id field must exist
    #     """

    #     assert 'id' in self.api_data['manager_user']


    # def test_api_field_type_manager_user_id(self):
    #     """ Test for type for API Field

    #     manager_user.id field must be int
    #     """

    #     assert type(self.api_data['manager_user']['id']) is int


    # def test_api_field_exists_manager_user_display_name(self):
    #     """ Test for existance of API Field

    #     manager_user.display_name field must exist
    #     """

    #     assert 'display_name' in self.api_data['manager_user']


    # def test_api_field_type_manager_user_display_name(self):
    #     """ Test for type for API Field

    #     manager_user.display_name field must be str
    #     """

    #     assert type(self.api_data['manager_user']['display_name']) is str


    # def test_api_field_exists_manager_user_url(self):
    #     """ Test for existance of API Field

    #     manager_user.url field must exist
    #     """

    #     assert 'url' in self.api_data['manager_user']


    # def test_api_field_type_manager_user_url(self):
    #     """ Test for type for API Field

    #     manager_user.url field must be Hyperlink
    #     """

    #     assert type(self.api_data['manager_user']['url']) is Hyperlink



    # def test_api_field_exists_manager_team(self):
    #     """ Test for existance of API Field

    #     manager_team field must exist
    #     """

    #     assert 'manager_team' in self.api_data


    # def test_api_field_type_manager_team(self):
    #     """ Test for type for API Field

    #     manager_team field must be dict
    #     """

    #     assert type(self.api_data['manager_team']) is dict


    # def test_api_field_exists_manager_team_id(self):
    #     """ Test for existance of API Field

    #     manager_team.id field must exist
    #     """

    #     assert 'id' in self.api_data['manager_team']


    # def test_api_field_type_manager_team_id(self):
    #     """ Test for type for API Field

    #     manager_team.id field must be int
    #     """

    #     assert type(self.api_data['manager_team']['id']) is int


    # def test_api_field_exists_manager_team_display_name(self):
    #     """ Test for existance of API Field

    #     manager_team.display_name field must exist
    #     """

    #     assert 'display_name' in self.api_data['manager_team']


    # def test_api_field_type_manager_team_display_name(self):
    #     """ Test for type for API Field

    #     manager_team.display_name field must be str
    #     """

    #     assert type(self.api_data['manager_team']['display_name']) is str


    # def test_api_field_exists_manager_team_url(self):
    #     """ Test for existance of API Field

    #     manager_team.url field must exist
    #     """

    #     assert 'url' in self.api_data['manager_team']


    # def test_api_field_type_manager_team_url(self):
    #     """ Test for type for API Field

    #     manager_team.url field must be str
    #     """

    #     assert type(self.api_data['manager_team']['url']) is str



    # def test_api_field_exists_team_members(self):
    #     """ Test for existance of API Field

    #     team_members field must exist
    #     """

    #     assert 'team_members' in self.api_data


    # def test_api_field_type_team_members(self):
    #     """ Test for type for API Field

    #     team_members field must be dict
    #     """

    #     assert type(self.api_data['team_members']) is list


    # def test_api_field_exists_team_members_id(self):
    #     """ Test for existance of API Field

    #     team_members.id field must exist
    #     """

    #     assert 'id' in self.api_data['team_members'][0]


    # def test_api_field_type_team_members_id(self):
    #     """ Test for type for API Field

    #     team_members.id field must be int
    #     """

    #     assert type(self.api_data['team_members'][0]['id']) is int


    # def test_api_field_exists_team_members_display_name(self):
    #     """ Test for existance of API Field

    #     team_members.display_name field must exist
    #     """

    #     assert 'display_name' in self.api_data['team_members'][0]


    # def test_api_field_type_team_members_display_name(self):
    #     """ Test for type for API Field

    #     team_members.display_name field must be str
    #     """

    #     assert type(self.api_data['team_members'][0]['display_name']) is str


    # def test_api_field_exists_team_members_url(self):
    #     """ Test for existance of API Field

    #     team_members.url field must exist
    #     """

    #     assert 'url' in self.api_data['team_members'][0]


    # def test_api_field_type_team_members_url(self):
    #     """ Test for type for API Field

    #     team_members.url field must be Hyperlink
    #     """

    #     assert type(self.api_data['team_members'][0]['url']) is Hyperlink
