import pytest

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from rest_framework.relations import Hyperlink

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_fields import APITenancyObject

from assistance.models.knowledge_base import KnowledgeBase, KnowledgeBaseCategory


class KnowledgeBaseAPI(
    TestCase,
    APITenancyObject
):

    model = KnowledgeBase

    app_namespace = 'v2'
    
    url_name = '_api_v2_knowledge_base'

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create the object
        2. create view user
        4. make api request
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        different_organization = Organization.objects.create(name='test_different_organization')


        self.view_team = Team.objects.create(
            organization=organization,
            team_name = 'teamone',
            model_notes = 'random note'
        )

        view_permissions = Permission.objects.get(
                codename = 'view_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        self.view_team.permissions.set([view_permissions])

        self.view_user = User.objects.create_user(username="test_user_view", password="password")



        self.item = self.model.objects.create(
            organization=organization,
            title = 'teamone',
            content = 'random note',
            summary = 'a summary',
            target_user = self.view_user,
            release_date = '2024-01-01 12:00:00',
            expiry_date = '2024-01-01 12:00:01',
            responsible_user = self.view_user,
            category = KnowledgeBaseCategory.objects.create(
                name='cat',
                target_user = self.view_user,
                organization=organization,
            )
        )

        self.item.responsible_teams.set([self.view_team])

        self.url_view_kwargs = {'pk': self.item.id}

        teamuser = TeamUsers.objects.create(
            team = self.view_team,
            user = self.view_user
        )

        organization.manager = self.view_user

        organization.save()

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data = response.data



    def test_api_field_exists_model_notes(self):
        """ Test for existance of API Field

        model_notes field does not exist for KB articles
        """

        assert 'model_notes' not in self.api_data


    def test_api_field_type_model_notes(self):
        """ Test for type for API Field

        model_notes does not exist for KB articles
        """

        pass



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

        category.display_name field must be int
        """

        assert type(self.api_data['category']['display_name']) is str


    def test_api_field_exists_category_url(self):
        """ Test for existance of API Field

        category.url field must exist
        """

        assert 'url' in self.api_data['category']


    def test_api_field_type_category_url(self):
        """ Test for type for API Field

        category.url field must be int
        """

        assert type(self.api_data['category']['url']) is str



    def test_api_field_exists_summary(self):
        """ Test for existance of API Field

        summary field must exist
        """

        assert 'summary' in self.api_data


    def test_api_field_type_summary(self):
        """ Test for type for API Field

        summary field must be str
        """

        assert type(self.api_data['summary']) is str



    def test_api_field_exists_content(self):
        """ Test for existance of API Field

        content field must exist
        """

        assert 'content' in self.api_data


    def test_api_field_type_summary(self):
        """ Test for type for API Field

        content field must be str
        """

        assert type(self.api_data['content']) is str



    def test_api_field_exists_release_date(self):
        """ Test for existance of API Field

        release_date field must exist
        """

        assert 'release_date' in self.api_data


    def test_api_field_type_release_date(self):
        """ Test for type for API Field

        release_date field must be str
        """

        assert type(self.api_data['release_date']) is str



    def test_api_field_exists_expiry_date(self):
        """ Test for existance of API Field

        expiry_date field must exist
        """

        assert 'expiry_date' in self.api_data


    def test_api_field_type_expiry_date(self):
        """ Test for type for API Field

        expiry_date field must be str
        """

        assert type(self.api_data['expiry_date']) is str



    def test_api_field_exists_public(self):
        """ Test for existance of API Field

        public field must exist
        """

        assert 'public' in self.api_data


    def test_api_field_type_public(self):
        """ Test for type for API Field

        public field must be bool
        """

        assert type(self.api_data['public']) is bool



    def test_api_field_type_target_user(self):
        """ Test for type for API Field

        target_user field must be dict
        """

        assert type(self.api_data['target_user']) is dict


    def test_api_field_exists_target_user_id(self):
        """ Test for existance of API Field

        target_user.id field must exist
        """

        assert 'id' in self.api_data['target_user']


    def test_api_field_type_target_user_id(self):
        """ Test for type for API Field

        target_user.id field must be int
        """

        assert type(self.api_data['target_user']['id']) is int


    def test_api_field_exists_target_user_display_name(self):
        """ Test for existance of API Field

        target_user.display_name field must exist
        """

        assert 'display_name' in self.api_data['target_user']


    def test_api_field_type_target_user_display_name(self):
        """ Test for type for API Field

        target_user.display_name field must be int
        """

        assert type(self.api_data['target_user']['display_name']) is str


    def test_api_field_exists_target_user_url(self):
        """ Test for existance of API Field

        target_user.url field must exist
        """

        assert 'url' in self.api_data['target_user']


    def test_api_field_type_target_user_url(self):
        """ Test for type for API Field

        target_user.url field must be int
        """

        assert type(self.api_data['target_user']['url']) is Hyperlink



    def test_api_field_type_responsible_user(self):
        """ Test for type for API Field

        responsible_user field must be dict
        """

        assert type(self.api_data['responsible_user']) is dict


    def test_api_field_exists_responsible_user_id(self):
        """ Test for existance of API Field

        responsible_user.id field must exist
        """

        assert 'id' in self.api_data['responsible_user']


    def test_api_field_type_responsible_user_id(self):
        """ Test for type for API Field

        responsible_user.id field must be int
        """

        assert type(self.api_data['responsible_user']['id']) is int


    def test_api_field_exists_responsible_user_display_name(self):
        """ Test for existance of API Field

        responsible_user.display_name field must exist
        """

        assert 'display_name' in self.api_data['responsible_user']


    def test_api_field_type_responsible_user_display_name(self):
        """ Test for type for API Field

        responsible_user.display_name field must be int
        """

        assert type(self.api_data['responsible_user']['display_name']) is str


    def test_api_field_exists_responsible_user_url(self):
        """ Test for existance of API Field

        responsible_user.url field must exist
        """

        assert 'url' in self.api_data['responsible_user']


    def test_api_field_type_responsible_user_url(self):
        """ Test for type for API Field

        responsible_user.url field must be Hyperlink
        """

        assert type(self.api_data['responsible_user']['url']) is Hyperlink



    def test_api_field_type_responsible_teams(self):
        """ Test for type for API Field

        responsible_teams field must be list
        """

        assert type(self.api_data['responsible_teams']) is list


    def test_api_field_exists_responsible_teams_id(self):
        """ Test for existance of API Field

        responsible_teams.id field must exist
        """

        assert 'id' in self.api_data['responsible_teams'][0]


    def test_api_field_type_responsible_teams_id(self):
        """ Test for type for API Field

        responsible_teams.id field must be int
        """

        assert type(self.api_data['responsible_teams'][0]['id']) is int


    def test_api_field_exists_responsible_teams_display_name(self):
        """ Test for existance of API Field

        responsible_teams.display_name field must exist
        """

        assert 'display_name' in self.api_data['responsible_teams'][0]


    def test_api_field_type_responsible_teams_display_name(self):
        """ Test for type for API Field

        responsible_teams.display_name field must be int
        """

        assert type(self.api_data['responsible_teams'][0]['display_name']) is str


    def test_api_field_exists_responsible_teams_url(self):
        """ Test for existance of API Field

        responsible_teams.url field must exist
        """

        assert 'url' in self.api_data['responsible_teams'][0]


    def test_api_field_type_responsible_teams_url(self):
        """ Test for type for API Field

        responsible_teams.url field must be str
        """

        assert type(self.api_data['responsible_teams'][0]['url']) is str
