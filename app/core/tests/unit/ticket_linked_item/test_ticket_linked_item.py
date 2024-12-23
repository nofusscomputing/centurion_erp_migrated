from django.contrib.auth.models import User
from django.test import Client, TestCase

from access.models import Organization

from assistance.models.knowledge_base import KnowledgeBase

from core.models.ticket.ticket_linked_items import Ticket, TicketLinkedItem

from config_management.models.groups import ConfigGroups

from itam.models.device import Device
from itam.models.operating_system import OperatingSystem
from itam.models.software import Software

from itim.models.clusters import Cluster
from itim.models.services import Service



class TicketLinkedItemBase:
    """ Test Cases common to ALL ticket types """

    ticket_type_enum = Ticket.TicketType.REQUEST

    item_type_enum = None


    @classmethod
    def CreateOrg(self):

        organization = Organization.objects.create(name='test_org')

        self.organization = organization


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create a ticket
        3. link the item to the ticket
        4. store the item id
        5. delete to item
        6. test to confirm `TicketLinkedItem` was cleaned up
        """

        self.user = User.objects.create_user(username="test_user_view", password="password")

        self.ticket = Ticket.objects.create(
            organization = self.organization,
            title = 'one',
            description = 'some text for body',
            opened_by = self.user,
            ticket_type = self.ticket_type_enum,
            status = Ticket.TicketStatus.All.NEW
        )

        self.item = TicketLinkedItem.objects.create(
            organization = self.organization,
            item = self.linked_item.id,
            item_type = self.item_type_enum,
            ticket = self.ticket,
        )

        self.item_id: int = self.linked_item.id

        self.linked_item.delete()




    def test_item_deleted_cleanup(self):

        items_found = TicketLinkedItem.objects.filter(
            item_type = self.item_type_enum,
            item = self.item_id
        )


        assert len(list(items_found)) == 0



class TicketLinkedItemCluster(
    TicketLinkedItemBase,
    TestCase
):

    item_type_enum = TicketLinkedItem.Modules.CLUSTER

    item_model = Cluster


    @classmethod
    def setUpTestData(self):


        self.CreateOrg()

        self.linked_item = self.item_model.objects.create(
            organization = self.organization,
            name = 'one',
        )

        super().setUpTestData()




class TicketLinkedItemConfigGroup(
    TicketLinkedItemBase,
    TestCase
):


    item_type_enum = TicketLinkedItem.Modules.CONFIG_GROUP

    item_model = ConfigGroups


    @classmethod
    def setUpTestData(self):

        self.CreateOrg()


        self.linked_item = self.item_model.objects.create(
            organization = self.organization,
            name = 'one',
        )

        super().setUpTestData()



class TicketLinkedItemDevice(
    TicketLinkedItemBase,
    TestCase
):

    item_type_enum = TicketLinkedItem.Modules.DEVICE

    item_model = Device


    @classmethod
    def setUpTestData(self):

        self.CreateOrg()

        self.linked_item = self.item_model.objects.create(
            organization = self.organization,
            name = 'one',
        )

        super().setUpTestData()



class TicketLinkedItemKB(
    TicketLinkedItemBase,
    TestCase
):

    item_type_enum = TicketLinkedItem.Modules.KB

    item_model = KnowledgeBase


    @classmethod
    def setUpTestData(self):

        self.CreateOrg()

        self.user_one = User.objects.create_user(username="user_one", password="password")

        self.user_two = User.objects.create_user(username="user_two", password="password")

        self.linked_item = self.item_model.objects.create(
            organization = self.organization,
            title = 'one',
            content = 'sadsadsads',
            target_user = self.user_one,
            responsible_user = self.user_two
        )


        super().setUpTestData()



class TicketLinkedItemOperatingSystem(
    TicketLinkedItemBase,
    TestCase
):

    item_type_enum = TicketLinkedItem.Modules.OPERATING_SYSTEM

    item_model = OperatingSystem


    @classmethod
    def setUpTestData(self):

        self.CreateOrg()

        self.linked_item = self.item_model.objects.create(
            organization = self.organization,
            name = 'one',
        )

        super().setUpTestData()



class TicketLinkedItemSoftware(
    TicketLinkedItemBase,
    TestCase
):

    item_type_enum = TicketLinkedItem.Modules.SOFTWARE

    item_model = Software


    @classmethod
    def setUpTestData(self):

        self.CreateOrg()

        self.linked_item = self.item_model.objects.create(
            organization = self.organization,
            name = 'one',
        )

        super().setUpTestData()



class TicketLinkedItemService(
    TicketLinkedItemBase,
    TestCase
):

    item_type_enum = TicketLinkedItem.Modules.SERVICE

    item_model = Service


    @classmethod
    def setUpTestData(self):

        self.CreateOrg()

        self.linked_item = self.item_model.objects.create(
            organization = self.organization,
            name = 'one',
        )

        super().setUpTestData()
