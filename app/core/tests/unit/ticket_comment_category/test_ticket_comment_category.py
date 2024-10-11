import pytest
# import unittest
# import requests

from django.test import TestCase

from app.tests.abstract.models import TenancyModel

from core.models.ticket.ticket_comment_category import TicketCommentCategory


class TicketCommentCategoryModel(
    TestCase,
    TenancyModel
):

    model = TicketCommentCategory


    # def test_attribute_duration_ticket_value(self):
    #     """Attribute value test

    #     This aattribute calculates the ticket duration from
    #     it's comments. must return total time in seconds
    #     """

    #     pass