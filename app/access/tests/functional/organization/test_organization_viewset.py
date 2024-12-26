import pytest
import unittest
import requests


from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_permissions_viewset import APIPermissions
from api.tests.abstract.api_serializer_viewset import SerializersTestCases
from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional, MetaDataNavigationEntriesFunctional



class ViewSetBase:

    model = Organization

    app_namespace = 'v2'
    
    url_name = '_api_v2_organization'

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

        self.item = organization

        different_organization = Organization.objects.create(name='test_different_organization')

        self.different_organization = different_organization

        self.other_org_item = organization

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

        view_team_b = Team.objects.create(
            team_name = 'view_team',
            organization = different_organization,
        )

        view_team.permissions.set([view_permissions])

        view_team_b.permissions.set([view_permissions])



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

        self.view_user_b = User.objects.create_user(username="test_user_view_b", password="password")
        teamuser = TeamUsers.objects.create(
            team = view_team_b,
            user = self.view_user_b
        )


        self.url_view_kwargs = { 'pk': self.item.id }

        self.add_data = {
            'name': 'team_post',
        }


        self.super_add_user = User.objects.create_user(username="test_user_add_super", password="password", is_superuser = True)

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



class OrganizationPermissionsAPI(
    ViewSetBase,
    APIPermissions,
    TestCase
):



    def test_add_has_permission(self):
        """ Check correct permission for add 

        Attempt to add as user with permission
        """

        client = Client()

        if self.url_kwargs:

            url = reverse( self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs )

        else:

            url = reverse( self.app_namespace + ':' + self.url_name + '-list' )


        client.force_login( self.add_user )

        response = client.post( url, data = self.add_data )

        assert response.status_code == 201



    def test_returned_results_only_user_orgs(self):
        """Returned results check

        This test case is an override of a test of the same name.
        organizations are not tenancy objects and therefor are supposed to
        return all items when a user queries them.

        Ensure that a query to the viewset endpoint does not return
        items that are not part of the users organizations.
        """


        # Ensure the other org item exists, without test not able to function
        print('Check that the different organization item has been defined')
        assert hasattr(self, 'other_org_item')

        # ensure that the variables for the two orgs are different orgs
        print('checking that the different and user oganizations are different')
        assert self.different_organization.id != self.organization.id


        client = Client()

        if self.url_kwargs:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')


        client.force_login(self.view_user)
        response = client.get(url)

        contains_different_org: bool = False

        # for item in response.data['results']:

        #     if int(item['id']) != self.organization.id:

        #         contains_different_org = True

        assert len(response.data['results']) == 2


    def test_add_different_organization_denied(self):
        """ Check correct permission for add

        This test is a duplicate of a test case with the same name.
        Organizations are not tenancy models so this test does nothing of value

        attempt to add as user from different organization
        """

        pass


class OrganizationViewSet(
    ViewSetBase,
    SerializersTestCases,
    TestCase
):

    pass



class OrganizationMetadata(
    ViewSetBase,
    MetadataAttributesFunctional,
    MetaDataNavigationEntriesFunctional,
    TestCase
):

    menu_id = 'access'

    menu_entry_id = 'organization'