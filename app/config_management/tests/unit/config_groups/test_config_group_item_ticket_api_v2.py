
from django.shortcuts import reverse
from django.test import Client, TestCase

from core.tests.abstract.test_item_ticket_api_v2 import ItemTicketAPI

from core.models.ticket.ticket_linked_items import TicketLinkedItem

from config_management.models.groups import ConfigGroups



class ConfigGroupsTicketAPI(
    ItemTicketAPI,
    TestCase,
):
    """Test Cases for Item Tickets

    Args:
        APITenancyObject (class): Base class for ALL field checks
    """

    item_type = TicketLinkedItem.Modules.CONFIG_GROUP

    item_class = 'config_group'

    item_model = ConfigGroups


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create an item

        """

        super().setUpTestData()


        self.linked_item = self.item_model.objects.create(
            organization = self.organization,
            name = 'dev'
        )



        self.item = self.model.objects.create(
            organization = self.organization,
            ticket = self.ticket,

            # Item attributes

            item = self.linked_item.id,
            item_type = self.item_type,
        )



        self.url_view_kwargs = {
            'item_class': self.item_class,
            'item_id': self.item.id,
            'pk': self.item.id,
        }


        client = Client()
        url = reverse('v2:_api_v2_item_tickets-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data = response.data



    def test_api_field_value_item_id(self):
        """ Test for existance of API Field

        item.id field must exist
        """

        assert  self.api_data['item']['id'] == self.linked_item.id



    def test_api_field_value_item_type(self):
        """ Test for type for API Field

        item_type field must be int
        """

        assert self.api_data['item_type'] == self.item_type

    def test_api_field_type_item_url(self):
        """ Test for type for API Field

        item.url field must be str
        """

        assert type(self.api_data['item']['url']) is str
