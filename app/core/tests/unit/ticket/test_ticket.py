import pytest
import unittest
import requests

from django.contrib.auth.models import User
from django.test import TestCase

from access.models import Organization

from app.tests.abstract.models import TenancyModel

from core.models.ticket.ticket import Ticket


class TicketModel(
    TestCase,
    TenancyModel
):

    model = Ticket

    should_model_history_be_saved: bool = False
    """Tickets should not save model history.

    Saving of model history is not required as a ticket stores it's
    history as an 'action comment'
    """


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a device
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.add_user = User.objects.create_user(username="test_user_add", password="password")


        self.item = self.model.objects.create(
            organization=organization,
            title = 'A ticket',
            description = 'the ticket body',
            ticket_type = Ticket.TicketType.REQUEST,
            opened_by = self.add_user,
            status = int(Ticket.TicketStatus.All.NEW.value)
        )

