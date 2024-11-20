from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_permissions_viewset import APIPermissions

from core.models.ticket.ticket_comment import Ticket, TicketComment

from settings.models.user_settings import UserSettings



class TicketCommentPermissionsAPI(
    APIPermissions,
    TestCase
):
    """ Test Cases common to ALL ticket types """

    model = TicketComment

    app_namespace = 'v2'
    
    change_data = {'body': 'it has changed'}

    delete_data = {}

    ticket_type: str = 'request'

    ticket_type_enum = Ticket.TicketType.REQUEST

    url_name = '_api_v2_ticket_comment'


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


        # import_permissions = Permission.objects.get(
        #         codename = 'import_' + self.model._meta.model_name,
        #         content_type = ContentType.objects.get(
        #             app_label = self.model._meta.app_label,
        #             model = self.model._meta.model_name,
        #         )
        #     )

        # import_team = Team.objects.create(
        #     team_name = 'import_team',
        #     organization = organization,
        # )

        # import_team.permissions.set([import_permissions])


        self.no_permissions_user = User.objects.create_user(username="test_no_permissions", password="password")


        self.view_user = User.objects.create_user(username="test_user_view", password="password")
        teamuser = TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )


        self.ticket = Ticket.objects.create(
            organization = self.organization,
            title = 'one',
            description = 'some text for body',
            opened_by = self.view_user,
            ticket_type = self.ticket_type_enum,
            status = Ticket.TicketStatus.All.NEW
        )

        self.item = self.model.objects.create(
            organization = self.organization,
            body = 'comment',
            ticket = self.ticket,
        )


        self.url_kwargs = {'ticket_id': self.ticket.id}

        self.url_view_kwargs = {'ticket_id': self.ticket.id, 'pk': self.item.id}

        self.add_data = {
            'organization': self.organization.id,
            'body': 'comment body',
            'ticket': self.ticket.id,
            'comment_type': int(TicketComment.CommentType.COMMENT)
        }


        self.add_user = User.objects.create_user(username="test_user_add", password="password")

        user_settings = UserSettings.objects.get(user=self.add_user)

        user_settings.default_organization = self.organization

        user_settings.save()


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


        # self.import_user = User.objects.create_user(username="test_user_import", password="password")
        # teamuser = TeamUsers.objects.create(
        #     team = import_team,
        #     user = self.import_user
        # )


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
