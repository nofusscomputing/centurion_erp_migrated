# import pytest

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from rest_framework.relations import Hyperlink

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_fields import APITenancyObject

from core.models.ticket.ticket_linked_items import Ticket, TicketLinkedItem

from itam.models.device import Device



class TicketLinkedItemAPI(
    TestCase,
    APITenancyObject
):

    model = TicketLinkedItem

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create an item

        """

        self.organization = Organization.objects.create(name='test_org')

        view_permissions = Permission.objects.get(
                codename = 'view_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        view_team = Team.objects.create(
            team_name = 'view_team',
            organization = self.organization,
        )

        view_team.permissions.set([view_permissions])

        self.view_user = User.objects.create_user(username="test_user_view", password="password")
        teamuser = TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )



        self.ticket = Ticket.objects.create(
            organization=self.organization,
            title = 'A ticket',
            description = 'the ticket body',
            opened_by = self.view_user,
            ticket_type = int(Ticket.TicketType.REQUEST.value),
        )

        device = Device.objects.create(
            organization = self.organization,
            name = 'dev'
        )



        self.item = self.model.objects.create(
            organization = self.organization,
            item = device.id,
            item_type = TicketLinkedItem.Modules.DEVICE,
            ticket = self.ticket
        )


        self.url_view_kwargs = {'ticket_id': self.ticket.id, 'pk': self.item.id}


        client = Client()
        url = reverse('v2:_api_v2_ticket_linked_item-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data = response.data





    def test_api_field_exists_model_notes(self):
        """ Test for existance of API Field

        This is a custom test of a test case with the same name.
        This model does not have this field.

        model_notes field must not exist
        """

        assert 'model_notes' not in self.api_data


    def test_api_field_type_model_notes(self):
        """ Test for type for API Field

        This is a custom test of a test case with the same name.
        This model does not have this field.
        """

        assert True



    def test_api_field_exists_modified(self):
        """ Test for existance of API Field

        This is a custom test of a test case with the same name.
        This model does not have this field.

        modified field must not exist
        """

        assert 'modified' not in self.api_data


    def test_api_field_type_modified(self):
        """ Test for type for API Field

        This is a custom test of a test case with the same name.
        This model does not have this field.
        """

        assert True



    def test_api_field_exists_item(self):
        """ Test for existance of API Field

        item field must exist
        """

        assert 'item' in self.api_data


    def test_api_field_type_item(self):
        """ Test for type for API Field

        item field must be dict
        """

        assert type(self.api_data['item']) is dict












    def test_api_field_exists_item_id(self):
        """ Test for existance of API Field

        item.id field must exist
        """

        assert 'id' in self.api_data['item']


    def test_api_field_type_item_id(self):
        """ Test for type for API Field

        item.id field must be int
        """

        assert type(self.api_data['item']['id']) is int


    def test_api_field_exists_item_display_name(self):
        """ Test for existance of API Field

        item.display_name field must exist
        """

        assert 'display_name' in self.api_data['item']


    def test_api_field_type_item_display_name(self):
        """ Test for type for API Field

        item.display_name field must be str
        """

        assert type(self.api_data['item']['display_name']) is str


    def test_api_field_exists_item_name(self):
        """ Test for existance of API Field

        item.name field must exist
        """

        assert 'name' in self.api_data['item']


    def test_api_field_type_item_name(self):
        """ Test for type for API Field

        item.name field must be str
        """

        assert type(self.api_data['item']['name']) is str



    def test_api_field_exists_item_url(self):
        """ Test for existance of API Field

        item.url field must exist
        """

        assert 'url' in self.api_data['item']


    def test_api_field_type_item_url(self):
        """ Test for type for API Field

        item.url field must be Hyperlink
        """

        assert type(self.api_data['item']['url']) is Hyperlink











    def test_api_field_exists_item_type(self):
        """ Test for existance of API Field

        item_type field must exist
        """

        assert 'item_type' in self.api_data


    def test_api_field_type_item_type(self):
        """ Test for type for API Field

        item_type field must be int
        """

        assert type(self.api_data['item_type']) is int



    def test_api_field_exists_ticket(self):
        """ Test for existance of API Field

        ticket field must exist
        """

        assert 'ticket' in self.api_data


    def test_api_field_type_ticket(self):
        """ Test for type for API Field

        ticket field must be dict
        """

        assert type(self.api_data['ticket']) is dict








    def test_api_field_exists_ticket_id(self):
        """ Test for existance of API Field

        ticket.id field must exist
        """

        assert 'id' in self.api_data['ticket']


    def test_api_field_type_ticket_id(self):
        """ Test for type for API Field

        ticket.id field must be int
        """

        assert type(self.api_data['ticket']['id']) is int


    def test_api_field_exists_ticket_display_name(self):
        """ Test for existance of API Field

        ticket.display_name field must exist
        """

        assert 'display_name' in self.api_data['ticket']


    def test_api_field_type_ticket_display_name(self):
        """ Test for type for API Field

        ticket.display_name field must be str
        """

        assert type(self.api_data['ticket']['display_name']) is str


    def test_api_field_exists_ticket_title(self):
        """ Test for existance of API Field

        ticket.title field must exist
        """

        assert 'title' in self.api_data['ticket']


    def test_api_field_type_ticket_title(self):
        """ Test for type for API Field

        ticket.title field must be str
        """

        assert type(self.api_data['ticket']['title']) is str



    def test_api_field_exists_ticket_url(self):
        """ Test for existance of API Field

        ticket.url field must exist
        """

        assert 'url' in self.api_data['ticket']


    def test_api_field_type_ticket_url(self):
        """ Test for type for API Field

        ticket.url field must be str
        """

        assert type(self.api_data['ticket']['url']) is str

