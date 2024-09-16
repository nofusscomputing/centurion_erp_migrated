import re

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import TestCase, Client

import pytest
import unittest
import requests

from access.models import Organization, Team, TeamUsers, Permission

from app.tests.abstract.model_permissions import ModelPermissions, ModelPermissionsAdd, ModelPermissionsChange

from project_management.models.projects import Project

from core.models.ticket import Ticket, RelatedTickets
from core.models.ticket.ticket_comment import TicketComment




class TicketCommentPermissions(
    # ModelPermissions,
    ModelPermissionsAdd,
    ModelPermissionsChange,
):

    ticket_type:str = None

    ticket_type_enum: int = None

    model = TicketComment

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
                codename = 'add_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        add_ticket_permissions = Permission.objects.get(
            codename = 'add_' + Ticket._meta.model_name + '_' + self.ticket_type,
            content_type = ContentType.objects.get(
                app_label = Ticket._meta.app_label,
                model = Ticket._meta.model_name,
            )
        )

        add_team = Team.objects.create(
            team_name = 'add_team',
            organization = organization,
        )

        add_team.permissions.set([add_ticket_permissions, add_permissions])


        self.add_user = User.objects.create_user(username="test_user_add", password="password")
        teamuser = TeamUsers.objects.create(
            team = add_team,
            user = self.add_user
        )


        self.ticket = Ticket.objects.create(
            organization=organization,
            title = 'A second ' + self.ticket_type + ' ticket',
            description = 'the ticket body of item two',
            ticket_type = int(Ticket.TicketType.REQUEST.value),
            opened_by = self.add_user,
            status = int(Ticket.TicketStatus.All.NEW.value)
        )

        self.item_add_user = self.model.objects.create(
            organization=organization,
            body = 'A ' + self.ticket_type + ' ticket comment',
            ticket = self.ticket,
            comment_type = int(TicketComment.CommentType.COMMENT),
            user = self.add_user,
            # status = int(Ticket.TicketStatus.All.NEW.value)
        )

        self.project = Project.objects.create(
            name = 'ticket permissions project name',
            organization = organization
        )


        self.url_add_kwargs = {'ticket_type': self.ticket_type, 'ticket_id': self.ticket.id}

        self.add_data = {
            'body': 'an add ticket',
            'comment_type': int(TicketComment.CommentType.COMMENT.value),
            'ticket': self.ticket.id,
            'organization': self.organization.id,
            'user': self.add_user.id,
        }


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

        self.change_team = change_team



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

        self.change_user = User.objects.create_user(username="test_user_change", password="password")
        teamuser = TeamUsers.objects.create(
            team = change_team,
            user = self.change_user
        )


        self.item = self.model.objects.create(
            organization=organization,
            body = 'A ' + self.ticket_type + ' ticket comment',
            ticket = self.ticket,
            comment_type = int(TicketComment.CommentType.COMMENT),
            user = self.change_user,
            # status = int(Ticket.TicketStatus.All.NEW.value)
        )


        self.url_view_kwargs = {'ticket_type': self.ticket_type, 'pk': self.item.id}

        self.url_change_kwargs = {'ticket_type': self.ticket_type, 'ticket_id': self.ticket.id, 'pk': self.item.id}

        self.change_data = {'body': 'a change to ticket commennt'}

        self.url_delete_kwargs = {'ticket_type': self.ticket_type, 'ticket_id': self.ticket.id, 'pk': self.item.id}

        self.delete_data = {'body': 'a delete to ticket'}


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


    def test_model_change_own_comment_has_permission(self):
        """ Check correct permission for change

        Make change with user who has add permission on own comment
        """

        client = Client()

        kwargs = self.url_change_kwargs.copy()

        kwargs['pk'] = self.item_add_user.id

        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=kwargs)


        client.force_login(self.add_user)
        response = client.post(url, data=self.change_data)

        assert response.status_code == 200



class ChangeTicketCommentPermissions(TicketCommentPermissions, TestCase):

    ticket_type = 'change'

    ticket_type_enum: int = int(Ticket.TicketType.CHANGE.value)

    app_namespace = 'ITIM'

    url_name_view = '_ticket_comment_change_view'

    url_name_add = '_ticket_comment_change_add'

    url_name_change = '_ticket_comment_change_change'

    url_name_delete = '_ticket_comment_change_delete'

    url_delete_response = reverse('ITIM:Changes')



class IncidentTicketCommentPermissions(TicketCommentPermissions, TestCase):

    ticket_type = 'incident'

    ticket_type_enum: int = int(Ticket.TicketType.INCIDENT.value)

    app_namespace = 'ITIM'

    url_name_view = '_ticket_comment_incident_view'

    url_name_add = '_ticket_comment_incident_add'

    url_name_change = '_ticket_comment_incident_change'

    url_name_delete = '_ticket_comment_incident_delete'

    url_delete_response = reverse('ITIM:Incidents')



class ProblemTicketCommentPermissions(TicketCommentPermissions, TestCase):

    ticket_type = 'problem'

    ticket_type_enum: int = int(Ticket.TicketType.PROBLEM.value)

    app_namespace = 'ITIM'

    url_name_view = '_ticket_comment_problem_view'

    url_name_add = '_ticket_comment_problem_add'

    url_name_change = '_ticket_comment_problem_change'

    url_name_delete = '_ticket_comment_problem_delete'

    url_delete_response = reverse('ITIM:Problems')



class RequestTicketCommentPermissions(TicketCommentPermissions, TestCase):

    ticket_type = 'request'

    ticket_type_enum: int = int(Ticket.TicketType.REQUEST.value)

    app_namespace = 'Assistance'

    url_name_view = '_ticket_comment_request_view'

    url_name_add = '_ticket_comment_request_add'

    url_name_change = '_ticket_comment_request_change'

    url_name_delete = '_ticket_comment_request_delete'

    url_delete_response = reverse('Assistance:Requests')
