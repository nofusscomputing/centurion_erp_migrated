import pytest

from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.exceptions import ValidationError

from access.models import Organization

from core.serializers.ticket_linked_item import Ticket, TicketLinkedItem, TicketLinkedItemModelSerializer

from itam.models.device import Device


class TicketLinkedItemValidationAPI(
    TestCase,
):

    model = TicketLinkedItem

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        2. Create an item
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.user = User.objects.create(
            username = 'user',
            password = 'password'
        )

        self.ticket = Ticket.objects.create(
            organization=organization,
            title = 'ticket title',
            description = 'some text',
            opened_by = self.user,
            status = Ticket.TicketStatus.All.NEW,
            ticket_type = Ticket.TicketType.REQUEST,
        )

        self.device = Device.objects.create(
            organization=organization,
            name = 'item',
        )

        self.device_two = Device.objects.create(
            organization=organization,
            name = 'item-two',
        )

        self.item = self.model.objects.create(
            organization=organization,
            ticket = self.ticket,
            item = self.device.id,
            item_type = TicketLinkedItem.Modules.DEVICE
        )



    def test_serializer_validation_add_valid_item(self):
        """Serializer Validation Check

        Ensure that a valid item it does not raise a validation error
        """

        class MockView:

            kwargs: dict = {
                'ticket_id': int(self.ticket.id)
            }


        serializer = TicketLinkedItemModelSerializer(
            context = {
                'view': MockView
            },
            data={
                "organization": self.organization.id,
                "ticket": self.ticket.id,
                "item_type": int(TicketLinkedItem.Modules.DEVICE),
                "item": self.device_two.id,
            }
        )

        assert serializer.is_valid(raise_exception = True)



    def test_serializer_validation_no_ticket(self):
        """Serializer Validation Check

        Ensure that a validation error is raised if no ticket specified.
        """

        with pytest.raises(ValidationError) as err:

            serializer = TicketLinkedItemModelSerializer(
                data={
                    "organization": self.organization.id,
                    # "ticket": self.ticket.id,
                    "item_type": int(TicketLinkedItem.Modules.DEVICE),
                    "item": self.device_two.id,
                }
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['ticket'] == 'required'



    def test_serializer_validation_no_item(self):
        """Serializer Validation Check

        Ensure that a validation error is raised if no ticket specified.
        """

        with pytest.raises(ValidationError) as err:

            serializer = TicketLinkedItemModelSerializer(
                data={
                    "organization": self.organization.id,
                    "ticket": self.ticket.id,
                    "item_type": int(TicketLinkedItem.Modules.DEVICE),
                    # "item": self.device_two.id,
                }
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['item'][0] == 'required'
