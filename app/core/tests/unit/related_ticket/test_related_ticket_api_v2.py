# import pytest

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from rest_framework.relations import Hyperlink

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_fields import APITenancyObject

from core.models.ticket.ticket import Ticket, RelatedTickets

from itam.models.device import Device



class RelatedTicketsLinkedItemAPI(
    TestCase,
    APITenancyObject
):

    model = RelatedTickets

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

        self.ticket_two = Ticket.objects.create(
            organization=self.organization,
            title = 'A ticket two',
            description = 'the ticket body',
            opened_by = self.view_user,
            ticket_type = int(Ticket.TicketType.REQUEST.value),
        )

        # device = Device.objects.create(
        #     organization = self.organization,
        #     name = 'dev'
        # )



        self.item = self.model.objects.create(
            organization = self.organization,
            from_ticket_id = self.ticket,
            to_ticket_id = self.ticket_two,
            how_related = RelatedTickets.Related.RELATED
        )


        self.url_view_kwargs = {'ticket_id': self.ticket.id, 'pk': self.item.id}


        client = Client()
        url = reverse('v2:_api_v2_ticket_related-detail', kwargs=self.url_view_kwargs)


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



    def test_api_field_exists_created(self):
        """ Test for existance of API Field

        This is a custom test of a test case with the same name.
        This model does not have this field.

        created field must not exist
        """

        assert 'created' not in self.api_data


    def test_api_field_type_created(self):
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



    def test_api_field_exists_from_ticket_id(self):
        """ Test for existance of API Field

        from_ticket_id field must exist
        """

        assert 'from_ticket_id' in self.api_data


    def test_api_field_type_from_ticket_id(self):
        """ Test for type for API Field

        from_ticket_id field must be dict
        """

        assert type(self.api_data['from_ticket_id']) is dict



    def test_api_field_exists_from_ticket_id_id(self):
        """ Test for existance of API Field

        from_ticket_id.id field must exist
        """

        assert 'id' in self.api_data['from_ticket_id']


    def test_api_field_type_from_ticket_id_id(self):
        """ Test for type for API Field

        from_ticket_id.id field must be int
        """

        assert type(self.api_data['from_ticket_id']['id']) is int


    def test_api_field_exists_from_ticket_id_display_name(self):
        """ Test for existance of API Field

        from_ticket_id.display_name field must exist
        """

        assert 'display_name' in self.api_data['from_ticket_id']


    def test_api_field_type_from_ticket_id_display_name(self):
        """ Test for type for API Field

        from_ticket_id.display_name field must be str
        """

        assert type(self.api_data['from_ticket_id']['display_name']) is str


    def test_api_field_exists_from_ticket_id_title(self):
        """ Test for existance of API Field

        from_ticket_id.title field must exist
        """

        assert 'title' in self.api_data['from_ticket_id']


    def test_api_field_type_from_ticket_id_title(self):
        """ Test for type for API Field

        from_ticket_id.title field must be str
        """

        assert type(self.api_data['from_ticket_id']['title']) is str



    def test_api_field_exists_from_ticket_id_url(self):
        """ Test for existance of API Field

        from_ticket_id.url field must exist
        """

        assert 'url' in self.api_data['from_ticket_id']


    def test_api_field_type_from_ticket_id_url(self):
        """ Test for type for API Field

        from_ticket_id.url field must be str
        """

        assert type(self.api_data['from_ticket_id']['url']) is str



    def test_api_field_exists_to_ticket_id(self):
        """ Test for existance of API Field

        to_ticket_id field must exist
        """

        assert 'to_ticket_id' in self.api_data


    def test_api_field_type_to_ticket_id(self):
        """ Test for type for API Field

        to_ticket_id field must be dict
        """

        assert type(self.api_data['to_ticket_id']) is dict



    def test_api_field_exists_to_ticket_id_id(self):
        """ Test for existance of API Field

        to_ticket_id.id field must exist
        """

        assert 'id' in self.api_data['to_ticket_id']


    def test_api_field_type_to_ticket_id_id(self):
        """ Test for type for API Field

        to_ticket_id.id field must be int
        """

        assert type(self.api_data['to_ticket_id']['id']) is int


    def test_api_field_exists_to_ticket_id_display_name(self):
        """ Test for existance of API Field

        to_ticket_id.display_name field must exist
        """

        assert 'display_name' in self.api_data['to_ticket_id']


    def test_api_field_type_to_ticket_id_display_name(self):
        """ Test for type for API Field

        to_ticket_id.display_name field must be str
        """

        assert type(self.api_data['to_ticket_id']['display_name']) is str


    def test_api_field_exists_to_ticket_id_title(self):
        """ Test for existance of API Field

        to_ticket_id.title field must exist
        """

        assert 'title' in self.api_data['to_ticket_id']


    def test_api_field_type_to_ticket_id_title(self):
        """ Test for type for API Field

        to_ticket_id.title field must be str
        """

        assert type(self.api_data['to_ticket_id']['title']) is str



    def test_api_field_exists_to_ticket_id_url(self):
        """ Test for existance of API Field

        to_ticket_id.url field must exist
        """

        assert 'url' in self.api_data['to_ticket_id']


    def test_api_field_type_to_ticket_id_url(self):
        """ Test for type for API Field

        to_ticket_id.url field must be str
        """

        assert type(self.api_data['to_ticket_id']['url']) is str



    def test_api_field_exists_how_related(self):
        """ Test for existance of API Field

        how_related field must exist
        """

        assert 'how_related' in self.api_data


    def test_api_field_type_how_related(self):
        """ Test for type for API Field

        how_related field must be int
        """

        assert type(self.api_data['how_related']) is int

