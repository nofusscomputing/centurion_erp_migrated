import celery
import pytest
import unittest
import requests

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import TestCase, Client
from django.test.utils import override_settings

from unittest.mock import patch

from access.models import Organization, Team, TeamUsers, Permission

from itam.models.device import Device

from settings.models.user_settings import UserSettings

class InventoryPermissionsAPI(TestCase):

    model = Device

    model_name = 'device'
    app_label = 'itam'

    inventory = {
        "details": {
            "name": "device_name",
            "serial_number": "a serial number",
            "uuid": "string"
        },
        "os": {
            "name": "os_name",
            "version_major": "12",
            "version": "12.1"
        },
        "software": [
            {
                "name": "software_name",
                "category": "category_name",
                "version": "1.2.3"
            }
        ]
    }

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


        # self.item = self.model.objects.create(
        #     organization=organization,
        #     name = 'deviceone'
        # )

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

        add_user_settings = UserSettings.objects.get(user=self.add_user)

        add_user_settings.default_organization = organization

        add_user_settings.save()

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



    @override_settings(CELERY_TASK_ALWAYS_EAGER=True,
                       CELERY_TASK_EAGER_PROPOGATES=True)
    def test_device_auth_add_user_anon_denied(self):
        """ Check correct permission for add 

        Attempt to add as anon user
        """

        client = Client()
        url = reverse('API:_api_device_inventory')


        response = client.put(url, data=self.inventory, content_type='application/json')

        assert response.status_code == 401


    @override_settings(CELERY_TASK_ALWAYS_EAGER=True,
                       CELERY_TASK_EAGER_PROPOGATES=True)
    def test_device_auth_add_no_permission_denied(self):
        """ Check correct permission for add

        Attempt to add as user with no permissions
        """

        client = Client()
        url = reverse('API:_api_device_inventory')


        client.force_login(self.no_permissions_user)
        response = client.post(url, data=self.inventory, content_type='application/json')

        assert response.status_code == 403


    @override_settings(CELERY_TASK_ALWAYS_EAGER=True,
                       CELERY_TASK_EAGER_PROPOGATES=True)
    def test_device_auth_add_different_organization_denied(self):
        """ Check correct permission for add

        attempt to add as user from different organization
        """

        client = Client()
        url = reverse('API:_api_device_inventory')


        client.force_login(self.different_organization_user)
        response = client.post(url, data=self.inventory, content_type='application/json')

        assert response.status_code == 403


    @override_settings(CELERY_TASK_ALWAYS_EAGER=True,
                       CELERY_TASK_EAGER_PROPOGATES=True)
    def test_device_auth_add_permission_view_denied(self):
        """ Check correct permission for add

        Attempt to add a user with view permission
        """

        client = Client()
        url = reverse('API:_api_device_inventory')


        client.force_login(self.view_user)
        response = client.post(url, data=self.inventory, content_type='application/json')

        assert response.status_code == 403


    @override_settings(CELERY_TASK_ALWAYS_EAGER=True,
                       CELERY_TASK_EAGER_PROPOGATES=True)
    def test_device_auth_add_has_permission(self):
        """ Check correct permission for add 

        Attempt to add as user with no permission
        """

        client = Client()
        url = reverse('API:_api_device_inventory')


        client.force_login(self.add_user)
        response = client.post(url, data=self.inventory, content_type='application/json')

        assert response.status_code == 200


