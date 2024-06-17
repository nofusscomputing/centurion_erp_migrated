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

from core.models.history import History


class OrganizationHistoryPermissions(TestCase):


    item_model = Organization


    model = History

    model_name = 'history'

    app_label = 'core'

    namespace = ''

    name_view = '_history'


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. create an organization that is different to item
        3. Create a device
        4. Add history device history entry as item
        5. create a user
        6. create user in different organization (with the required permission)
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        different_organization = Organization.objects.create(name='test_different_organization')

        self.item = self.organization

        self.history_model_name = self.item._meta.model_name

        self.history = self.model.objects.get(
            item_pk = self.item.id,
            item_class = self.item._meta.model_name,
            action = self.model.Actions.ADD,
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


        self.no_permissions_user = User.objects.create_user(username="test_no_permissions", password="password")


        self.view_user = User.objects.create_user(username="test_user_view", password="password")
        teamuser = TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )

        self.different_organization_user = User.objects.create_user(username="test_different_organization_user", password="password")


        different_organization_team = Team.objects.create(
            team_name = 'different_organization_team',
            organization = different_organization,
        )

        different_organization_team.permissions.set([
            view_permissions,
        ])

        TeamUsers.objects.create(
            team = different_organization_team,
            user = self.different_organization_user
        )



    def test_auth_view_history_user_anon_denied(self):
        """ Check correct permission for view

        Attempt to view as anon user
        """

        client = Client()
        url = reverse(self.namespace + self.name_view, kwargs={'model_name': self.history_model_name, 'model_pk': self.item.id})

        response = client.get(url)

        assert response.status_code == 302 and response.url.startswith('/account/login')


    def test_auth_view_history_no_permission_denied(self):
        """ Check correct permission for view

        Attempt to view with user missing permission
        """

        client = Client()
        url = reverse(self.namespace +  self.name_view, kwargs={'model_name': self.history_model_name, 'model_pk': self.item.id})


        client.force_login(self.no_permissions_user)
        response = client.get(url)

        assert response.status_code == 403


    def test_auth_view_history_different_organizaiton_denied(self):
        """ Check correct permission for view

        Attempt to view with user from different organization
        """

        client = Client()
        url = reverse(self.namespace +  self.name_view, kwargs={'model_name': self.history_model_name, 'model_pk': self.item.id})


        client.force_login(self.different_organization_user)
        response = client.get(url)

        assert response.status_code == 403


    def test_auth_view_history_has_permission(self):
        """ Check correct permission for view

        Attempt to view as user with view permission
        """

        client = Client()
        url = reverse(self.namespace +  self.name_view, kwargs={'model_name': self.history_model_name, 'model_pk': self.item.id})


        client.force_login(self.view_user)
        response = client.get(url)

        assert response.status_code == 200
