from django.shortcuts import reverse
from django.test import Client, TestCase

from rest_framework.relations import Hyperlink

from core.tests.abstract.test_ticket_api_v2 import TicketAPI

from core.models.ticket.ticket import Ticket



class ProjectTaskTicketAPI(
    TicketAPI,
    TestCase
):

    model = Ticket

    ticket_type = 'project_task'

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create an item

        """

        super().setUpTestData()


        self.item = self.model.objects.create(

            # All Tickets
            organization=self.organization,
            title = 'A ' + self.ticket_type + ' ticket',
            description = 'the ticket body',
            opened_by = self.view_user,
            status = int(Ticket.TicketStatus.All.CLOSED.value),
            project = self.project,
            milestone = self.project_milestone,
            external_ref = 1,
            external_system = Ticket.Ticket_ExternalSystem.CUSTOM_1,
            date_closed = '2024-01-01T01:02:03Z',

            # ITIL Tickets
            category = self.ticket_category,

            # Specific to ticket
            ticket_type = int(Ticket.TicketType.PROJECT_TASK.value),
        )

        self.item.assigned_teams.set([ self.view_team ])

        self.item.assigned_users.set([ self.view_user ])

        self.item.subscribed_teams.set([ self.view_team ])

        self.item.subscribed_users.set([ self.view_user ])


        self.url_kwargs = {'project_id': self.project.id}
        self.url_view_kwargs = {'project_id': self.project.id, 'pk': self.item.id}

        client = Client()
        url = reverse('v2:_api_v2_ticket_' + self.ticket_type + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data = response.data



    def test_api_field_exists_impact(self):
        """ Test for existance of API Field

        impact field must exist
        """

        assert 'impact' in self.api_data


    def test_api_field_type_impact(self):
        """ Test for type for API Field

        impact field must be int
        """

        assert type(self.api_data['impact']) is int



    def test_api_field_exists_category(self):
        """ Test for existance of API Field

        category field must exist
        """

        assert 'category' in self.api_data


    def test_api_field_type_category(self):
        """ Test for type for API Field

        category field must be dict
        """

        assert type(self.api_data['category']) is dict


    def test_api_field_exists_category_display_name(self):
        """ Test for existance of API Field

        category.display_name field must exist
        """

        assert 'display_name' in self.api_data['category']


    def test_api_field_type_category_display_name(self):
        """ Test for type for API Field

        category.display_name field must be str
        """

        assert type(self.api_data['category']['display_name']) is str


    def test_api_field_exists_category_url(self):
        """ Test for existance of API Field

        category.url field must exist
        """

        assert 'url' in self.api_data['category']


    def test_api_field_type_category_url(self):
        """ Test for type for API Field

        category.url field must be Hyperlink
        """

        assert type(self.api_data['category']['url']) is Hyperlink
