import pytest
import unittest
import requests

from django.contrib.auth.models import AnonymousUser, User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from access.models import Organization, Team, TeamUsers, Permission

from core.tests.abstract.history_permissions import HistoryPermissions

from itam.models.device import Device



class DeviceHistoryPermissions(TestCase, HistoryPermissions):


    item_model = Device


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

        self.item = self.item_model.objects.create(
            organization=organization,
            name = 'deviceone'
        )

        self.history = self.model.objects.get(
            item_pk = self.item.id,
            item_class = self.item._meta.model_name,
            action = self.model.Actions.ADD,
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
