import pytest

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_permissions_viewset import APIPermissions

from core.models.notes import Notes

from config_management.models.groups import ConfigGroups



class NoteViewSetCommon(
    APIPermissions
):

    app_namespace: str = None
    
    url_name: str = None

    change_data = {'note': 'a changed note'}

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
                codename = 'view_' + Notes._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = Notes._meta.app_label,
                    model = Notes._meta.model_name,
                )
            )

        view_team = Team.objects.create(
            team_name = 'view_team',
            organization = organization,
        )

        view_team.permissions.set([view_permissions])



        add_permissions = Permission.objects.get(
                codename = 'add_' + Notes._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = Notes._meta.app_label,
                    model = Notes._meta.model_name,
                )
            )

        add_team = Team.objects.create(
            team_name = 'add_team',
            organization = organization,
        )

        add_team.permissions.set([add_permissions])



        change_permissions = Permission.objects.get(
                codename = 'change_' + Notes._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = Notes._meta.app_label,
                    model = Notes._meta.model_name,
                )
            )

        change_team = Team.objects.create(
            team_name = 'change_team',
            organization = organization,
        )

        change_team.permissions.set([change_permissions])



        delete_permissions = Permission.objects.get(
                codename = 'delete_' + Notes._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = Notes._meta.app_label,
                    model = Notes._meta.model_name,
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





        # self.note_item = ConfigGroups.objects.create(
        #     organization = self.organization,
        #     name = 'history-device'
        # )


        # self.item = Notes.objects.create(
        #     organization = self.organization,
        #     note = 'a note',
        #     usercreated = self.view_user,
        #     config_group = self.note_item
        # )


        # self.url_kwargs = {'group_id': self.note_item.id}

        # self.url_view_kwargs = {'group_id': self.note_item.id, 'pk': self.item.pk }

        # self.add_data = {'note': 'a note added', 'organization': self.organization.id}
