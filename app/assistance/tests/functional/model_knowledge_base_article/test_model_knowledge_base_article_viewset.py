import pytest
import unittest
import requests


from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.contenttypes.models import ContentType
from django.test import Client, TestCase

from rest_framework.reverse import reverse

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_permissions_viewset import (
    APIPermissionAdd,
    APIPermissionDelete,
    APIPermissionView
)

from api.tests.abstract.api_serializer_viewset import SerializersTestCases
from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional, MetaDataNavigationEntriesFunctional

from assistance.models.model_knowledge_base_article import KnowledgeBase, ModelKnowledgeBaseArticle

from itam.models.device import Device



class ViewSetBase:

    model = ModelKnowledgeBaseArticle

    app_namespace = 'v2'
    
    url_name = '_api_v2_model_kb'

    change_data = {'title': 'device'}

    delete_data = {}

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a team
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        different_organization = Organization.objects.create(name='test_different_organization')

        self.different_organization = different_organization


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



        add_permissions = Permission.objects.get(
                codename = 'add_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        add_team = Team.objects.create(
            team_name = 'add_team',
            organization = organization,
        )

        add_team.permissions.set([add_permissions])



        delete_permissions = Permission.objects.get(
                codename = 'delete_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        delete_team = Team.objects.create(
            team_name = 'delete_team',
            organization = organization,
        )

        delete_team.permissions.set([delete_permissions])


        self.no_permissions_user = User.objects.create_user(username="test_no_permissions", password="password")


        self.view_user = User.objects.create_user(username="test_user_view", password="password")
        self.view_user_b = User.objects.create_user(username="test_user_view_b", password="password")
        teamuser = TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )


        knowledge_base = KnowledgeBase.objects.create(
            organization = self.organization,
            title = 'title',
            content = 'sdfsdf'
        )

        knowledge_base_same_org_two = KnowledgeBase.objects.create(
            organization = self.organization,
            title = 'title',
            content = 'sdfsdf'
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

        knowledge_base_two = KnowledgeBase.objects.create(
            organization = self.organization,
            title = 'title two',
            content = 'sdfsdf'
        )

        device_two = Device.objects.create(
            organization = self.different_organization,
            name = 'device two'
        )


        self.other_org_item = self.model.objects.create(
            organization = self.different_organization,
            article = knowledge_base_two,
            model = str( device._meta.app_label ) + '.' + str( device._meta.model_name ),
            model_pk = device_two.id
        )


        self.url_kwargs = {
            'model': 'device',
            'model_pk': device.id,
        }

        self.url_view_kwargs = {
            'model': 'device',
            'model_pk': device.id,
            'pk': self.item.id
        }

        self.add_data = {
            'article': knowledge_base_same_org_two.id,
            'organization': self.organization.id,
            'model': 'device',
            'model_pk': device.id
        }


        self.add_user = User.objects.create_user(username="test_user_add", password="password")
        teamuser = TeamUsers.objects.create(
            team = add_team,
            user = self.add_user
        )


        self.delete_user = User.objects.create_user(username="test_user_delete", password="password")
        teamuser = TeamUsers.objects.create(
            team = delete_team,
            user = self.delete_user
        )


        self.different_organization_user = User.objects.create_user(username="test_different_organization_user", password="password")


        different_organization_team = Team.objects.create(
            team_name = 'different_organization_team',
            organization = different_organization,
        )

        different_organization_team.permissions.set([
            view_permissions,
            add_permissions,
            delete_permissions,
        ])

        TeamUsers.objects.create(
            team = different_organization_team,
            user = self.different_organization_user
        )


class ModelKnowledgeBaseArticlePermissionsAPI(
    ViewSetBase,
    APIPermissionAdd,
    APIPermissionDelete,
    APIPermissionView,
    TestCase,
):

    pass


class ModelKnowledgeBaseArticleViewSet(
    ViewSetBase,
    SerializersTestCases,
    TestCase,
):


    @pytest.mark.skip( reason = 'not required' )
    def test_returned_serializer_user_change(self):
        """This model does not have a change user"""

        pass



class ModelKnowledgeBaseArticleMetadata(
    ViewSetBase,
    MetadataAttributesFunctional,
    MetaDataNavigationEntriesFunctional,
    TestCase
):

    menu_id = 'assistance'

    menu_entry_id = 'knowledge_base'


    @pytest.mark.skip( reason = 'not required' )
    def test_navigation_entry_change_user(self):
        """ this model does not have nor require a menu entry
        
        This model does not have a change user
        """

        pass


    @pytest.mark.skip( reason = 'not required' )
    def test_navigation_no_empty_menu_change_user(self):
        """ this model does not have nor require a menu entry
        
        This model does not have a change user
        """

        pass


    @pytest.mark.skip( reason = 'not required' )
    def test_navigation_entry_view_user(self):
        """ this model does not have nor require a menu entry
        
        This model does not have a change user
        """

        pass


    @pytest.mark.skip( reason = 'not required' )
    def test_method_options_request_detail_data_key_urls_self_is_str(self):
        """This model does not require a self url as it does not
        
        have a change user nor is designed to change.
        """

        pass


    def test_method_options_request_detail_data_key_urls_self_not_exist(self):
        """Test HTTP/Options Method

        Ensure the request data key `urls.self` does not exist
        """

        client = Client()
        client.force_login(self.view_user)

        response = client.options(
            reverse(
                self.app_namespace + ':' + self.url_name + '-detail',
                kwargs=self.url_view_kwargs
            ),
            content_type='application/json'
        )

        assert 'self' not in response.data['urls']
