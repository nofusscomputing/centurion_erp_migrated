# from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import TestCase, Client

import pytest
import unittest
import requests

from access.models import Organization, Team, TeamUsers, Permission
from access.tests.abstract.model_permissions_organization_manager import OrganizationManagerModelPermissionAdd, OrganizationManagerModelPermissionDelete

from app.tests.abstract.model_permissions import ModelPermissionsAdd, ModelPermissionsChange, ModelPermissionsDelete



class TeamUserPermissions(
    TestCase,
    ModelPermissionsAdd,
    ModelPermissionsDelete,
    OrganizationManagerModelPermissionAdd,
    OrganizationManagerModelPermissionDelete
):

    model = TeamUsers

    app_namespace = 'Access'

    url_name_view = '_team_user_view'

    url_name_add = '_team_user_add'

    url_name_change = '_team_user_view'

    url_name_delete = '_team_user_delete'


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a device
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        different_organization = Organization.objects.create(name='test_different_organization')

        self.different_organization = different_organization

        self.test_team = Team.objects.create(
            team_name = 'test_team',
            organization = organization,
        )

        self.team_user = User.objects.create_user(username="test_self.team_user", password="password")

        self.item = self.model.objects.create(
            team = self.test_team,
            user = self.team_user
        )


        self.url_view_kwargs = {'pk': self.item.id}

        self.url_add_kwargs = {'organization_id': self.organization.id, 'pk': self.item.id}

        self.add_data = {'operating_system': 'operating_system', 'organization': self.organization.id}

        self.url_change_kwargs = {'organization_id': self.organization.id, 'team_id': self.item.team.id, 'pk': self.item.id}

        self.change_data = {'operating_system': 'operating_system', 'organization': self.organization.id}

        self.url_delete_kwargs = {'organization_id': self.organization.id, 'team_id': self.item.team.id, 'pk': self.item.id}

        self.delete_data = {'operating_system': 'operating_system', 'organization': self.organization.id}

        self.url_delete_response = reverse('Access:_team_view', 
            kwargs={
                'organization_id': self.organization.id,
                'pk': self.test_team.id
            }
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

        self.user_is_organization_manager = User.objects.create_user(
            username="test_org_manager",
            password="password"
        )

        self.organization.manager = self.user_is_organization_manager
        self.organization.save()

        self.different_organization_is_manager = User.objects.create_user(
            username="test_org_manager_different_org",
            password="password"
        )

        self.different_organization.manager = self.different_organization_is_manager
        self.different_organization.save()



    @pytest.mark.skip(reason="feature does not exist")
    def test_team_user_auth_change_user_anon_denied(self):
        """ Check correct permission for change

        Attempt to change as anon
        """

        client = Client()
        url = reverse('Access:_team_user_view', kwargs={'pk': self.item.id})


        response = client.patch(url, data={'device': 'device'})

        assert response.status_code == 302 and response.url.startswith('/account/login')


    @pytest.mark.skip(reason="feature does not exist")
    def test_team_user_auth_change_no_permission_denied(self):
        """ Ensure permission view cant make change

        Attempt to make change as user without permissions
        """

        client = Client()
        url = reverse('Access:_team_user_view', kwargs={'pk': self.item.id})


        client.force_login(self.no_permissions_user)
        response = client.post(url, data={'device': 'device'})

        assert response.status_code == 403


    @pytest.mark.skip(reason="feature does not exist")
    def test_team_user_auth_change_different_organization_denied(self):
        """ Ensure permission view cant make change

        Attempt to make change as user from different organization
        """

        client = Client()
        url = reverse('Access:_team_user_view', kwargs={'pk': self.item.id})


        client.force_login(self.different_organization_user)
        response = client.post(url, data={'device': 'device'})

        assert response.status_code == 403


    @pytest.mark.skip(reason="feature does not exist")
    def test_team_user_auth_change_permission_view_denied(self):
        """ Ensure permission view cant make change

        Attempt to make change as user with view permission
        """

        client = Client()
        url = reverse('Access:_team_user_view', kwargs={'pk': self.item.id})


        client.force_login(self.view_user)
        response = client.post(url, data={'device': 'device'})

        assert response.status_code == 403


    @pytest.mark.skip(reason="feature does not exist")
    def test_team_user_auth_change_permission_add_denied(self):
        """ Ensure permission view cant make change

        Attempt to make change as user with add permission
        """

        client = Client()
        url = reverse('Access:_team_user_view', kwargs={'pk': self.item.id})


        client.force_login(self.add_user)
        response = client.post(url, data={'device': 'device'})

        assert response.status_code == 403


    @pytest.mark.skip(reason="feature does not exist")
    def test_team_user_auth_change_has_permission(self):
        """ Check correct permission for change

        Make change with user who has change permission
        """

        client = Client()
        url = reverse('Access:_team_user_view', kwargs={'pk': self.item.id})


        client.force_login(self.change_user)
        response = client.post(url, data={'device': 'device'})

        assert response.status_code == 200
