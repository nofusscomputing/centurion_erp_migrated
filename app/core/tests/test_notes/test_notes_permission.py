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
from itam.models.device import Device


@pytest.mark.skip(reason="this test needs to move to models tests that recieve notes")
class NotesPermissions(TestCase):

    model = Device

    model_name = 'device'
    app_label = 'itam'

    namespace = 'ITAM'

    name_view = '_device_view'

    name_add = '_device_add'

    name_change = '_device_view'

    name_delete = '_device_delete'

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


        self.item = self.model.objects.create(
            organization=organization,
            name = 'deviceone'
        )

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



    def test_auth_view_user_anon_denied(self):
        """ Check correct permission for view

        Attempt to view as anon user
        """

        client = Client()
        url = reverse(self.namespace + ':' + self.name_view, kwargs={'pk': self.item.id})

        response = client.get(url)

        assert response.status_code == 302 and response.url.startswith('/account/login')


    def test_auth_view_no_permission_denied(self):
        """ Check correct permission for view

        Attempt to view with user missing permission
        """

        client = Client()
        url = reverse(self.namespace + ':' + self.name_view, kwargs={'pk': self.item.id})


        client.force_login(self.no_permissions_user)
        response = client.get(url)

        assert response.status_code == 403


    def test_auth_view_different_organizaiton_denied(self):
        """ Check correct permission for view

        Attempt to view with user from different organization
        """

        client = Client()
        url = reverse(self.namespace + ':' + self.name_view, kwargs={'pk': self.item.id})


        client.force_login(self.different_organization_user)
        response = client.get(url)

        assert response.status_code == 403


    def test_auth_view_has_permission(self):
        """ Check correct permission for view

        Attempt to view as user with view permission
        """

        client = Client()
        url = reverse(self.namespace + ':' + self.name_view, kwargs={'pk': self.item.id})


        client.force_login(self.view_user)
        response = client.get(url)

        assert response.status_code == 200



    def test_auth_add_user_anon_denied(self):
        """ Check correct permission for add 

        Attempt to add as anon user
        """

        client = Client()
        url = reverse(self.namespace + ':' + self.name_add)


        response = client.put(url, data={'device': 'device'})

        assert response.status_code == 302 and response.url.startswith('/account/login')

    # @pytest.mark.skip(reason="ToDO: figure out why fails")
    def test_auth_add_no_permission_denied(self):
        """ Check correct permission for add

        Attempt to add as user with no permissions
        """

        client = Client()
        url = reverse(self.namespace + ':' + self.name_add)


        client.force_login(self.no_permissions_user)
        response = client.post(url, data={'device': 'device'})

        assert response.status_code == 403


    # @pytest.mark.skip(reason="ToDO: figure out why fails")
    def test_auth_add_different_organization_denied(self):
        """ Check correct permission for add

        attempt to add as user from different organization
        """

        client = Client()
        url = reverse(self.namespace + ':' + self.name_add)


        client.force_login(self.different_organization_user)
        response = client.post(url, data={'name': 'device', 'organization': self.organization.id})

        assert response.status_code == 403


    def test_auth_add_permission_view_denied(self):
        """ Check correct permission for add

        Attempt to add a user with view permission
        """

        client = Client()
        url = reverse(self.namespace + ':' + self.name_add)


        client.force_login(self.view_user)
        response = client.post(url, data={'device': 'device'})

        assert response.status_code == 403


    def test_auth_add_has_permission(self):
        """ Check correct permission for add 

        Attempt to add as user with no permission
        """

        client = Client()
        url = reverse(self.namespace + ':' + self.name_add)


        client.force_login(self.add_user)
        response = client.post(url, data={'device': 'device', 'organization': self.organization.id})

        assert response.status_code == 200



    def test_auth_change_user_anon_denied(self):
        """ Check correct permission for change

        Attempt to change as anon
        """

        client = Client()
        url = reverse(self.namespace + ':' + self.name_view, kwargs={'pk': self.item.id})


        response = client.patch(url, data={'device': 'device'})

        assert response.status_code == 302 and response.url.startswith('/account/login')


    def test_auth_change_no_permission_denied(self):
        """ Ensure permission view cant make change

        Attempt to make change as user without permissions
        """

        client = Client()
        url = reverse(self.namespace + ':' + self.name_view, kwargs={'pk': self.item.id})


        client.force_login(self.no_permissions_user)
        response = client.post(url, data={'device': 'device'})

        assert response.status_code == 403


    def test_auth_change_different_organization_denied(self):
        """ Ensure permission view cant make change

        Attempt to make change as user from different organization
        """

        client = Client()
        url = reverse(self.namespace + ':' + self.name_view, kwargs={'pk': self.item.id})


        client.force_login(self.different_organization_user)
        response = client.post(url, data={'device': 'device'})

        assert response.status_code == 403


    def test_auth_change_permission_view_denied(self):
        """ Ensure permission view cant make change

        Attempt to make change as user with view permission
        """

        client = Client()
        url = reverse(self.namespace + ':' + self.name_view, kwargs={'pk': self.item.id})


        client.force_login(self.view_user)
        response = client.post(url, data={'device': 'device'})

        assert response.status_code == 403


    def test_auth_change_permission_add_denied(self):
        """ Ensure permission view cant make change

        Attempt to make change as user with add permission
        """

        client = Client()
        url = reverse(self.namespace + ':' + self.name_view, kwargs={'pk': self.item.id})


        client.force_login(self.add_user)
        response = client.post(url, data={'device': 'device'})

        assert response.status_code == 403


    def test_auth_change_has_permission(self):
        """ Check correct permission for change

        Make change with user who has change permission
        """

        client = Client()
        url = reverse(self.namespace + ':' + self.name_view, kwargs={'pk': self.item.id})


        client.force_login(self.change_user)
        response = client.post(url, data={'device': 'device'})

        assert response.status_code == 200



    def test_auth_delete_user_anon_denied(self):
        """ Check correct permission for delete

        Attempt to delete item as anon user
        """

        client = Client()
        url = reverse(self.namespace + ':' + self.name_delete, kwargs={'pk': self.item.id})


        response = client.delete(url, data={'device': 'device'})

        assert response.status_code == 302 and response.url.startswith('/account/login')


    def test_auth_delete_no_permission_denied(self):
        """ Check correct permission for delete

        Attempt to delete as user with no permissons
        """

        client = Client()
        url = reverse(self.namespace + ':' + self.name_delete, kwargs={'pk': self.item.id})


        client.force_login(self.no_permissions_user)
        response = client.delete(url, data={'device': 'device'})

        assert response.status_code == 403


    def test_auth_delete_different_organization_denied(self):
        """ Check correct permission for delete

        Attempt to delete as user from different organization
        """

        client = Client()
        url = reverse(self.namespace + ':' + self.name_delete, kwargs={'pk': self.item.id})


        client.force_login(self.different_organization_user)
        response = client.delete(url, data={'device': 'device'})

        assert response.status_code == 403


    def test_auth_delete_permission_view_denied(self):
        """ Check correct permission for delete

        Attempt to delete as user with veiw permission only
        """

        client = Client()
        url = reverse(self.namespace + ':' + self.name_delete, kwargs={'pk': self.item.id})


        client.force_login(self.view_user)
        response = client.delete(url, data={'device': 'device'})

        assert response.status_code == 403


    def test_auth_delete_permission_add_denied(self):
        """ Check correct permission for delete

        Attempt to delete as user with add permission only
        """

        client = Client()
        url = reverse(self.namespace + ':' + self.name_delete, kwargs={'pk': self.item.id})


        client.force_login(self.add_user)
        response = client.delete(url, data={'device': 'device'})

        assert response.status_code == 403


    def test_auth_delete_permission_change_denied(self):
        """ Check correct permission for delete

        Attempt to delete as user with change permission only
        """

        client = Client()
        url = reverse(self.namespace + ':' + self.name_delete, kwargs={'pk': self.item.id})


        client.force_login(self.change_user)
        response = client.delete(url, data={'device': 'device'})

        assert response.status_code == 403


    def test_auth_delete_has_permission(self):
        """ Check correct permission for delete

        Delete item as user with delete permission
        """

        client = Client()
        url = reverse(self.namespace + ':' + self.name_delete, kwargs={'pk': self.item.id})


        client.force_login(self.delete_user)
        response = client.delete(url, data={'device': 'device'})

        assert response.status_code == 302 and response.url == reverse(self.namespace + ':Devices')
