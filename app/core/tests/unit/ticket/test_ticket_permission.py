# from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.contenttypes.models import ContentType
# from django.core.exceptions import ValidationError
from django.shortcuts import reverse
from django.test import TestCase, Client

import pytest
import unittest
import requests

from access.models import Organization, Team, TeamUsers, Permission

from app.tests.abstract.model_permissions import ModelPermissions

from project_management.models.projects import Project

from core.models.ticket.ticket import Ticket

from core.tests.unit.ticket.ticket_permission.field_based_permissions import TicketFieldBasedPermissions




class TicketPermissions(
    ModelPermissions,
    TicketFieldBasedPermissions
):

    ticket_type:str = None

    ticket_type_enum: int = None

    model = Ticket

    # app_namespace = 'Assistance'

    # url_name_view = '_ticket_request_view'

    # url_name_add = '_ticket_request_add'

    # url_name_change = '_ticket_request_change'

    # url_name_delete = '_ticket_request_delete'

    # url_delete_response = reverse('Assistance:Requests')

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a manufacturer
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        different_organization = Organization.objects.create(name='test_different_organization')


        add_permissions = Permission.objects.get(
                codename = 'add_' + self.model._meta.model_name + '_' + self.ticket_type,
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


        self.add_user = User.objects.create_user(username="test_user_add", password="password")
        teamuser = TeamUsers.objects.create(
            team = add_team,
            user = self.add_user
        )


        self.item = self.model.objects.create(
            organization=organization,
            title = 'A ' + self.ticket_type + ' ticket',
            description = 'the ticket body',
            ticket_type = int(Ticket.TicketType.REQUEST.value),
            opened_by = self.add_user,
            status = int(Ticket.TicketStatus.All.NEW.value)
        )

        self.project = Project.objects.create(
            name = 'ticket permissions project name',
            organization = organization
        )


        self.url_view_kwargs = {'ticket_type': self.ticket_type, 'pk': self.item.id}

        self.url_add_kwargs = {'ticket_type': self.ticket_type}

        self.add_data = {
            'title': 'an add ticket',
            'organization': self.organization.id,
            'opened_by': self.add_user.id,
        }

        self.url_change_kwargs = {'ticket_type': self.ticket_type, 'pk': self.item.id}

        self.change_data = {'title': 'an change to ticket'}

        self.url_delete_kwargs = {'ticket_type': self.ticket_type, 'pk': self.item.id}

        self.delete_data = {'title': 'a delete to ticket'}


        view_permissions = Permission.objects.get(
                codename = 'view_' + self.model._meta.model_name + '_' + self.ticket_type,
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


        change_permissions = Permission.objects.get(
                codename = 'change_' + self.model._meta.model_name + '_' + self.ticket_type,
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
                codename = 'delete_' + self.model._meta.model_name + '_' + self.ticket_type,
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

        # Import user/permissions

        import_permissions = Permission.objects.get(
                codename = 'import_' + self.model._meta.model_name + '_' + self.ticket_type,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        import_team = Team.objects.create(
            team_name = 'import_team',
            organization = organization,
        )

        import_team.permissions.set([change_permissions, import_permissions])


        self.import_user = User.objects.create_user(username="test_user_import", password="password")
        teamuser = TeamUsers.objects.create(
            team = import_team,
            user = self.import_user
        )

        # Triage user/permissions

        triage_permissions = Permission.objects.get(
                codename = 'triage_' + self.model._meta.model_name + '_' + self.ticket_type,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        triage_team = Team.objects.create(
            team_name = 'triage_team',
            organization = organization,
        )

        triage_team.permissions.set([change_permissions, triage_permissions])


        self.triage_user = User.objects.create_user(username="test_user_triage", password="password")
        teamuser = TeamUsers.objects.create(
            team = triage_team,
            user = self.triage_user
        )




    @pytest.mark.skip(reason="To be written")
    def test_permission_triage(self):

        pass


    @pytest.mark.skip(reason="To be written")
    def test_permission_purge(self):

        pass



    @pytest.mark.skip(reason='to be written')
    def test_ticket_action_comment_assign_user_added(self):
        """Action Comment test
        Confirm an action comment is created when a user is added as assigned
        """

        pass


    @pytest.mark.skip(reason='to be written')
    def test_ticket_action_comment_assign_user_removed(self):
        """Action Comment test
        Confirm an action comment is created when a user is removed as assigned
        """

        pass


    @pytest.mark.skip(reason='to be written')
    def test_ticket_action_comment_assign_team_added(self):
        """Action Comment test
        Confirm an action comment is created when a team is added as assigned
        """

        pass


    @pytest.mark.skip(reason='to be written')
    def test_ticket_action_comment_assign_team_removed(self):
        """Action Comment test
        Confirm an action comment is created when a team is removed as assigned
        """

        pass



    @pytest.mark.skip(reason='to be written')
    def test_ticket_action_comment_subscribe_user_added(self):
        """Action Comment test
        Confirm an action comment is created when a user is added as subscribed
        """

        pass


    @pytest.mark.skip(reason='to be written')
    def test_ticket_action_comment_subscribe_user_removed(self):
        """Action Comment test
        Confirm an action comment is created when a user is removed as subscribed
        """

        pass


    @pytest.mark.skip(reason='to be written')
    def test_ticket_action_comment_subscribe_team_added(self):
        """Action Comment test
        Confirm an action comment is created when a team is added as subscribed
        """

        pass


    @pytest.mark.skip(reason='to be written')
    def test_ticket_action_comment_subscribe_team_removed(self):
        """Action Comment test
        Confirm an action comment is created when a team is removed as subscribed
        """

        pass



    @pytest.mark.skip(reason='to be written')
    def test_ticket_action_comment_status_change(self):
        """Action Comment test
        Confirm an action comment is created when the ticket status changes
        """

        pass



    @pytest.mark.skip(reason='to be written')
    def test_ticket_action_comment_related_ticket_added(self):
        """Action Comment test
        Confirm an action comment is created when a related ticket is added
        """

        pass


    @pytest.mark.skip(reason='to be written')
    def test_ticket_action_comment_related_ticket_removed(self):
        """Action Comment test
        Confirm an action comment is created when a related ticket is removed
        """

        pass


    @pytest.mark.skip(reason='to be written')
    def test_ticket_creation_field_edit_denied(self):
        """Action Comment test
        Confirm an action comment is created when a user is added as assigned
        """

        pass




class ChangeTicketPermissions(TicketPermissions, TestCase):

    ticket_type = 'change'

    ticket_type_enum: int = int(Ticket.TicketType.CHANGE.value)

    app_namespace = 'ITIM'

    url_name_view = '_ticket_change_view'

    url_name_add = '_ticket_change_add'

    url_name_change = '_ticket_change_change'

    url_name_delete = '_ticket_change_delete'

    url_delete_response = reverse('ITIM:Changes')



class IncidentTicketPermissions(TicketPermissions, TestCase):

    ticket_type = 'incident'

    ticket_type_enum: int = int(Ticket.TicketType.INCIDENT.value)

    app_namespace = 'ITIM'

    url_name_view = '_ticket_incident_view'

    url_name_add = '_ticket_incident_add'

    url_name_change = '_ticket_incident_change'

    url_name_delete = '_ticket_incident_delete'

    url_delete_response = reverse('ITIM:Incidents')



class ProblemTicketPermissions(TicketPermissions, TestCase):

    ticket_type = 'problem'

    ticket_type_enum: int = int(Ticket.TicketType.PROBLEM.value)

    app_namespace = 'ITIM'

    url_name_view = '_ticket_problem_view'

    url_name_add = '_ticket_problem_add'

    url_name_change = '_ticket_problem_change'

    url_name_delete = '_ticket_problem_delete'

    url_delete_response = reverse('ITIM:Problems')



class RequestTicketPermissions(TicketPermissions, TestCase):

    ticket_type = 'request'

    ticket_type_enum: int = int(Ticket.TicketType.REQUEST.value)

    app_namespace = 'Assistance'

    url_name_view = '_ticket_request_view'

    url_name_add = '_ticket_request_add'

    url_name_change = '_ticket_request_change'

    url_name_delete = '_ticket_request_delete'

    url_delete_response = reverse('Assistance:Requests')
