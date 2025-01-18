import pytest

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from rest_framework.relations import Hyperlink

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_fields import APITenancyObject

from assistance.models.model_knowledge_base_article import KnowledgeBase, ModelKnowledgeBaseArticle
from assistance.models.knowledge_base import KnowledgeBaseCategory

from itam.models.device import Device



class ModelKnowledgeBaseArticleAPI(
    APITenancyObject,
    TestCase,
):

    model = ModelKnowledgeBaseArticle

    app_namespace = 'v2'
    
    url_name = '_api_v2_model_kb'

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


        knowledge_base = KnowledgeBase.objects.create(
            organization = self.organization,
            title = 'title',
            content = 'sdfsdf',
            category = KnowledgeBaseCategory.objects.create(
                organization = self.organization,
                name = 'cat',
            )
        )

        device = Device.objects.create(
            organization = self.organization,
            name = 'device'
        )


        self.item = self.model.objects.create(
            organization = self.organization,
            article = knowledge_base,
            model = str( device._meta.app_label ) + '.' + str( device._meta.model_name ),
            model_pk = device.id
        )

        self.url_view_kwargs = {
            'model': 'device',
            'model_pk': device.id,
            'pk': self.item.id
        }

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



    @pytest.mark.skip( reason = 'not required for this model' )
    def test_api_field_exists_display_name(self):
        """ Test for existance of API Field

        display_name field must exist
        """

        pass


    @pytest.mark.skip( reason = 'not required for this model' )
    def test_api_field_type_display_name(self):
        """ Test for type for API Field

        display_name field must be str
        """

        pass



    @pytest.mark.skip( reason = 'not required for this model' )
    def test_api_field_exists_model_notes(self):
        """ Test for existance of API Field

        model_notes field does not exist for KB articles
        """

        pass


    def test_api_field_not_exists_model_notes(self):
        """ Test for existance of API Field

        model_notes field does not exist for KB articles
        """

        assert 'model_notes' not in self.api_data


    @pytest.mark.skip( reason = 'not required for this model' )
    def test_api_field_type_model_notes(self):
        """ Test for type for API Field

        model_notes does not exist for KB articles
        """

        pass



    @pytest.mark.skip( reason = 'not required for this model' )
    def test_api_field_exists_urls(self):
        """ Test for existance of API Field

        _urls field must exist
        """

        pass


    @pytest.mark.skip( reason = 'not required for this model' )
    def test_api_field_type_urls(self):
        """ Test for type for API Field

        _urls field must be str
        """

        pass


    @pytest.mark.skip( reason = 'not required for this model' )
    def test_api_field_exists_urls_self(self):
        """ Test for existance of API Field

        _urls._self field must exist
        """

        pass


    @pytest.mark.skip( reason = 'not required for this model' )
    def test_api_field_type_urls(self):
        """ Test for type for API Field

        _urls._self field must be str
        """

        pass




    def test_api_field_exists_article(self):
        """ Test for existance of API Field

        article field must exist
        """

        assert 'article' in self.api_data


    def test_api_field_type_article(self):
        """ Test for type for API Field

        article field must be dict
        """

        assert type(self.api_data['article']) is dict


    def test_api_field_exists_article_id(self):
        """ Test for existance of API Field

        article.id field must exist
        """

        assert 'id' in self.api_data['article']


    def test_api_field_type_article_id(self):
        """ Test for type for API Field

        article.id field must be int
        """

        assert type(self.api_data['article']['id']) is int


    def test_api_field_exists_article_display_name(self):
        """ Test for existance of API Field

        article.display_name field must exist
        """

        assert 'display_name' in self.api_data['article']


    def test_api_field_type_article_display_name(self):
        """ Test for type for API Field

        article.display_name field must be int
        """

        assert type(self.api_data['article']['display_name']) is str


    def test_api_field_exists_article_url(self):
        """ Test for existance of API Field

        article.url field must exist
        """

        assert 'url' in self.api_data['article']


    def test_api_field_type_article_url(self):
        """ Test for type for API Field

        article.url field must be int
        """

        assert type(self.api_data['article']['url']) is str



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

        category.id field must be dict
        """

        assert type(self.api_data['category']['id']) is int



    def test_api_field_exists_category_display_name(self):
        """ Test for existance of API Field

        category.display_name field must exist
        """

        assert 'display_name' in self.api_data['category']


    def test_api_field_type_category_display_name(self):
        """ Test for type for API Field

        category.display_name field must be dict
        """

        assert type(self.api_data['category']['display_name']) is str



    def test_api_field_exists_category_name(self):
        """ Test for existance of API Field

        category.name field must exist
        """

        assert 'name' in self.api_data['category']


    def test_api_field_type_category_name(self):
        """ Test for type for API Field

        category.name field must be dict
        """

        assert type(self.api_data['category']['name']) is str



    def test_api_field_exists_category_url(self):
        """ Test for existance of API Field

        category.url field must exist
        """

        assert 'url' in self.api_data['category']


    def test_api_field_type_category_url(self):
        """ Test for type for API Field

        category.url field must be dict
        """

        assert type(self.api_data['category']['url']) is str
