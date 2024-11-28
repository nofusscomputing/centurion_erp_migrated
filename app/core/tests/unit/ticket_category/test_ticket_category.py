import pytest
# import unittest
# import requests

from django.test import TestCase

from access.models import Organization

from app.tests.abstract.models import TenancyModel

from core.models.ticket.ticket_category import TicketCategory


class TicketCategoryModel(
    TestCase,
    TenancyModel
):

    model = TicketCategory


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


        self.item = self.model.objects.create(
            organization=organization,
            name = 'cat',
        )


    # def test_attribute_duration_ticket_value(self):
    #     """Attribute value test

    #     This aattribute calculates the ticket duration from
    #     it's comments. must return total time in seconds
    #     """

    #     pass