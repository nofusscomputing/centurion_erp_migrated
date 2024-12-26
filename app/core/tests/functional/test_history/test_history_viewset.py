import pytest
# import unittest
# import requests


# from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_permissions_viewset import APIPermissionView
from api.tests.abstract.test_metadata_functional import (
    MetadataAttributesFunctionalBase,
    MetadataAttributesFunctionalEndpoint,
)

from core.models.history import History

from itam.models.device import Device



class ViewSetBase:

    model = History

    app_namespace = 'v2'
    
    url_name = '_api_v2_model_history'

    change_data = {'name': 'device'}

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



        change_permissions = Permission.objects.get(
                codename = 'change_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        change_team = Team.objects.create(
            team_name = 'change_team',
            organization = organization,
        )

        change_team.permissions.set([change_permissions])



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
        teamuser = TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )


        # self.config_group = ConfigGroups.objects.create(
        #     organization = self.organization,
        #     name = 'one'
        # )

        # self.software = Software.objects.create(
        #     organization = self.organization,
        #     name = 'random name'
        # )

        # self.software_two = Software.objects.create(
        #     organization = self.organization,
        #     name = 'random name two'
        # )

        # self.software_version = SoftwareVersion.objects.create(
        #     organization = self.organization,
        #     software = self.software,
        #     name = '1.1.1'
        # )


        # self.software_version_two = SoftwareVersion.objects.create(
        #     organization = self.organization,
        #     software = self.software_two,
        #     name = '2.2.2'
        # )

        self.device = Device.objects.create(
            organization = self.organization,
            name = 'history-device'
        )


        # self.item = self.model.objects.create(
        #     organization = self.organization,
        #     config_group = self.config_group,
        #     software = self.software,
        #     version = self.software_version
        # )

        self.item = History.objects.get(item_class = 'device', item_pk = self.device.id)


        self.url_kwargs = {'model_class': 'device', 'model_id': self.device.id}

        self.url_view_kwargs = {'model_class': 'device', 'model_id': self.device.id, 'pk': self.item.pk }

        self.add_data = {}


        self.add_user = User.objects.create_user(username="test_user_add", password="password")
        teamuser = TeamUsers.objects.create(
            team = add_team,
            user = self.add_user
        )

        self.change_user = User.objects.create_user(username="test_user_change", password="password")
        teamuser = TeamUsers.objects.create(
            team = change_team,
            user = self.change_user
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
            change_permissions,
            delete_permissions,
        ])

        TeamUsers.objects.create(
            team = different_organization_team,
            user = self.different_organization_user
        )



class HistoryPermissionsAPI(
    ViewSetBase,
    APIPermissionView,
    TestCase
):


    def test_view_list_has_permission(self):
        """ Check correct permission for view

        Attempt to view as user with view permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs=self.url_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        assert response.status_code == 200


    def test_view_has_permission(self):
        """ Check correct permission for view

        Custom permission of test case with same name.
        This test ensures that the user is denied

        Attempt to view as user with view permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        assert response.status_code == 200


    def test_add_has_permission_method_not_allowed(self):
        """ Check correct permission for add 

        Custom permission of test case with same name.
        This test ensures that the user is denied

        Attempt to add as user with permission
        """

        client = Client()
        if self.url_kwargs:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')


        client.force_login(self.add_user)
        response = client.post(url, data=self.add_data)

        assert response.status_code == 405



    def test_change_has_permission_method_not_allowed(self):
        """ Check correct permission for change

        Custom permission of test case with same name.
        This test ensures that the user is denied

        Make change with user who has change permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.change_user)
        response = client.patch(url, data=self.change_data, content_type='application/json')

        assert response.status_code == 405


    def test_delete_has_permission_method_not_allowed(self):
        """ Check correct permission for delete

        Custom permission of test case with same name.
        This test ensures that the user is denied

        Delete item as user with delete permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.delete_user)
        response = client.delete(url, data=self.delete_data)

        assert response.status_code == 405


    def test_returned_results_only_user_orgs(self):
        """Test not required

        this test is not required as a history item obtains it's
        organization from the object changed.
        """

        pass


    # item is not tenancy object
    def test_view_different_organizaiton_denied(self):
        """ Check correct permission for view

        This test case is a duplicate of a test case with the same name. This
        test is not required as currently the history model is not a tenancy
        model.
        
        see https://github.com/nofusscomputing/centurion_erp/issues/455 for
        more details.

        Attempt to view with user from different organization
        """

        pass


class HistoryMetadata(
    ViewSetBase,
    MetadataAttributesFunctionalEndpoint,
    MetadataAttributesFunctionalBase,
    TestCase
):




    def test_method_options_request_detail_data_has_key_urls_self(self):
        """Test HTTP/Options Method

        This is a custom test of a test with the same name.
        history view has no detail view, due to using a custom
        view "history",

        Ensure the request data returned has key `urls.self`
        """

        client = Client()
        client.force_login(self.view_user)

        response = client.options(
            reverse(
                self.app_namespace + ':' + self.url_name + '-list',
                kwargs=self.url_kwargs
            ),
            content_type='application/json'
        )

        assert 'urls' in response.data


    def test_method_options_request_detail_data_key_urls_self_is_str(self):
        """Test HTTP/Options Method

        This is a custom test of a test with the same name.
        history view has no detail view, due to using a custom
        view "history",

        Ensure the request data key `urls.self` is a string
        """

        client = Client()
        client.force_login(self.view_user)

        response = client.options(
            reverse(
                self.app_namespace + ':' + self.url_name + '-list',
                kwargs=self.url_kwargs
            ),
            content_type='application/json'
        )

        assert type(response.data['urls']['self']) is str
