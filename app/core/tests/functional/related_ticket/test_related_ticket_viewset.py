import pytest
import unittest
import requests


from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_permissions_viewset import (
    APIPermissionDelete,
    APIPermissionView,
)
from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional

from core.models.ticket.ticket import Ticket, RelatedTickets



class ViewSetBase:

    model = RelatedTickets

    app_namespace = 'v2'
    
    url_name = '_api_v2_ticket_related'

    change_data = {'from_ticket_id': 1, 'organization': 1,}

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


        self.no_permissions_user = User.objects.create_user(username="test_no_permissions", password="password")


        self.view_user = User.objects.create_user(username="test_user_view", password="password")
        teamuser = TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )

        ticket_one = Ticket.objects.create(
            organization = self.organization,
            title = 'A ticket',
            description = 'the ticket body',
            ticket_type = Ticket.TicketType.REQUEST,
            opened_by = self.view_user,
            status = Ticket.TicketStatus.All.NEW.value
        )

        ticket_two = Ticket.objects.create(
            organization = self.organization,
            title = 'B ticket',
            description = 'the ticket body',
            ticket_type = Ticket.TicketType.REQUEST,
            opened_by = self.view_user,
            status = Ticket.TicketStatus.All.NEW.value
        )


        self.item = self.model.objects.create(
            organization = self.organization,
            from_ticket_id = ticket_one,
            to_ticket_id = ticket_two,
            how_related = RelatedTickets.Related.BLOCKS
        )


        self.url_view_kwargs = {'ticket_id': ticket_one.id, 'pk': self.item.id}

        self.url_kwargs = {'ticket_id': ticket_one.id}

        self.add_data = {
            'organization': self.organization.id,
            'from_ticket_id': ticket_two.id,
            'to_ticket_id': ticket_one.id,
            'how_related': RelatedTickets.Related.RELATED
        }


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



class RelatedTicketsPermissionsAPI(
    ViewSetBase,
    APIPermissionDelete,
    APIPermissionView,
    TestCase,
):

    def test_add_has_permission_post_not_allowed(self):
        """ Check correct permission for add 

        Attempt to add as user with permission
        """

        client = Client()
        if self.url_kwargs:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')


        client.force_login(self.add_user)
        response = client.post(url, data=self.add_data)

        assert response.status_code == 405



    def test_change_has_permission_patch_not_allowed(self):
        """ Check correct permission for change

        Make change with user who has change permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.change_user)
        response = client.patch(url, data=self.change_data, content_type='application/json')

        assert response.status_code == 405



    def test_change_has_permission_put_not_allowed(self):
        """ Check correct permission for change

        Make change with user who has change permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.change_user)
        response = client.put(url, data=self.change_data, content_type='application/json')

        assert response.status_code == 405


    def test_returned_results_only_user_orgs(self):
        """Test not required

        this test is not required as a related ticket obtains it's
        organization from the ticket.
        """

        pass



class RelatedTicketsMetadata(
    ViewSetBase,
    MetadataAttributesFunctional,
    TestCase
):

    pass
