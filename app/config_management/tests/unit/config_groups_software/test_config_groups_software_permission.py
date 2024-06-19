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

from app.tests.abstract.model_permissions import ModelPermissionsAdd, ModelPermissionsChange, ModelPermissionsDelete

from config_management.models.groups import ConfigGroups, ConfigGroupSoftware

from itam.models.device import DeviceSoftware
from itam.models.software import Software



class ConfigGroupSoftwarePermissions(TestCase, ModelPermissionsAdd, ModelPermissionsChange, ModelPermissionsDelete):

    model = ConfigGroupSoftware
    parent_model = ConfigGroups

    model_name = 'configgroupsoftware'
    app_label = 'config_management'

    app_namespace = 'Config Management'

    url_name_view = '_group_view'

    url_name_add = '_group_software_add'

    url_name_change = '_group_software_change'

    url_name_delete = '_group_software_delete'


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. create an organization that is different to item
        3. Create the parent item
        4. create a software item
        5. create the item
        6. create teams with each permission: view, add, change, delete
        7. create a user per team
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        different_organization = Organization.objects.create(name='test_different_organization')


        self.parent_item = self.parent_model.objects.create(
            organization=organization,
            name = 'group_one'
        )

        self.software_item = Software.objects.create(
            organization=organization,
            name = 'softwareone',
        )

        self.item = self.model.objects.create(
            organization = organization,
            software = self.software_item,
            config_group = self.parent_item,
            action = DeviceSoftware.Actions.INSTALL
        )


        self.url_view_kwargs = {'pk': self.item.id}

        self.url_add_kwargs = {'pk': self.parent_item.id,}

        self.add_data = {'device': 'device', 'organization': self.organization.id}

        self.url_change_kwargs = {'pk': self.item.id, 'group_id': self.parent_item.id}

        self.change_data = {'device': 'device', 'organization': self.organization.id}

        self.url_delete_kwargs = {'pk': self.item.id, 'group_id': self.parent_item.id}

        self.delete_data = {'device': 'device', 'organization': self.organization.id}

        self.url_delete_response = reverse('Config Management:_group_view', kwargs={'pk': self.parent_item.id})

        view_permissions = Permission.objects.get(
                codename = 'view_' + self.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.app_label,
                    model = self.model_name,
                )
            )

        view_team = Team.objects.create(
            team_name = 'view_team',
            organization = organization,
        )

        view_team.permissions.set([view_permissions])



        add_permissions = Permission.objects.get(
                codename = 'add_' + self.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.app_label,
                    model = self.model_name,
                )
            )

        add_team = Team.objects.create(
            team_name = 'add_team',
            organization = organization,
        )

        add_team.permissions.set([add_permissions])



        change_permissions = Permission.objects.get(
                codename = 'change_' + self.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.app_label,
                    model = self.model_name,
                )
            )

        change_team = Team.objects.create(
            team_name = 'change_team',
            organization = organization,
        )

        change_team.permissions.set([change_permissions])



        delete_permissions = Permission.objects.get(
                codename = 'delete_' + self.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.app_label,
                    model = self.model_name,
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


    @pytest.mark.skip(reason="figure out best way to test")
    def test_config_groups_auth_view_user_anon_denied(self):
        """ Check correct permission for view

        Attempt to view as anon user
        """

        client = Client()
        url = reverse('Config Management:_group_view', kwargs={'pk': self.item.id})

        response = client.get(url)

        assert response.status_code == 302 and response.url.startswith('/account/login')


    @pytest.mark.skip(reason="figure out best way to test")
    def test_config_groups_auth_view_no_permission_denied(self):
        """ Check correct permission for view

        Attempt to view with user missing permission
        """

        client = Client()
        url = reverse('Config Management:_group_view', kwargs={'pk': self.item.id})


        client.force_login(self.no_permissions_user)
        response = client.get(url)

        assert response.status_code == 403


    @pytest.mark.skip(reason="figure out best way to test")
    def test_config_groups_auth_view_different_organizaiton_denied(self):
        """ Check correct permission for view

        Attempt to view with user from different organization
        """

        client = Client()
        url = reverse('Config Management:_group_view', kwargs={'pk': self.item.id})


        client.force_login(self.different_organization_user)
        response = client.get(url)

        assert response.status_code == 403


    @pytest.mark.skip(reason="figure out best way to test")
    def test_config_groups_auth_view_has_permission(self):
        """ Check correct permission for view

        Attempt to view as user with view permission
        """

        client = Client()
        url = reverse('Config Management:_group_view', kwargs={'pk': self.item.id})


        client.force_login(self.view_user)
        response = client.get(url)

        assert response.status_code == 200



    @pytest.mark.skip(reason="ToDO: refactor abstract test case")
    def test_model_change_has_permission(self):

        # this test requires re-write for 302 redirection
        # actual test
        # assert response.status_code == 302 and response.url == reverse('Config Management:_group_view', kwargs={'pk': self.parent_item.id})

        pass
