
import pytest
import unittest
import requests

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import TestCase, Client

from access.models import Organization, Team, TeamUsers, Permission

from settings.models.user_settings import UserSettings

class UserSettings(TestCase):


    model = UserSettings

    model_name = 'usersettings'
    app_label = 'settings'


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


        self.item = self.model.objects.get(
            user=self.view_user,
        )




    def test_user_settings_exist(self):
        """ User Settings must exist for user

        User settings a created if they dont exist on attempting to access
        """

        assert self.item


    def test_user_settings_organization_is_none(self):
        """ User Settings value 'organization' is none

        When row is created the organization must not be set
        """

        assert self.item.default_organization_id is None


    def test_user_settings_organization_edit_correct(self):
        """ User Settings value 'organization' is none

        When row is created the organization must not be set
        """

        self.item.default_organization_id = self.different_organization.id

        self.item.save()

        assert self.item.default_organization_id == self.different_organization.id


    # @pytest.mark.skip(reason="to be written")
    def test_user_settings_on_delete_of_user_settings_removed(self):
        """ On Delete of a user their settings are removed """
        
        test_user = User.objects.create_user(username="test_user_single_use", password="password")

        assert self.model.objects.get(
            user=test_user,
        )

        test_user.delete()


        settings = self.model.objects.filter(
            user_id=test_user.id,
        )

        assert settings.exists() == False


    @pytest.mark.skip(reason="to be written")
    def test_user_settings_on_delete_organization_default_organization(self):
        """ On Delete of an organization, users default organization set to null """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_user_settings_on_delete_organization_user_settings_not_deleted(self):
        """ On Delete of an organization, users settings are not deleted """
        pass
