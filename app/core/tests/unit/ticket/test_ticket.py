import pytest
import unittest
import requests

from django.test import TestCase

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


    @pytest.mark.skip(reason='test to be written')
    def test_attribute_duration_ticket_value(self):
        """Attribute value test

        This aattribute calculates the ticket duration from
        it's comments. must return total time in seconds
        """

        pass


    @pytest.mark.skip(reason='test to be written')
    def test_ticket_create_add_opened_by_as_watcher_ui(self):
        """New ticket action from UI

        When a new ticket is created, the 'opened_by' user must be added
        as a subscribed user.
        """

        pass


    @pytest.mark.skip(reason='test to be written')
    def test_ticket_create_add_opened_by_as_watcher_api(self):
        """New ticket action from API

        When a new ticket is created, the 'opened_by' user must be added
        as a subscribed user.
        """

        pass


    @pytest.mark.skip(reason='test to be written')
    def test_field_milestone_no_project(self):
        """Field Value Test

        Ensure that a milestone can't be applied if no project
        has been selected
        """

        pass


    @pytest.mark.skip(reason='test to be written')
    def test_field_milestone_has_project(self):
        """Field Value Test

        Ensure that a milestone can be applied if a project
        has been selected
        """

        pass


    @pytest.mark.skip(reason='test to be written')
    def test_field_milestone_different_project(self):
        """Field Value Test

        Ensure that a milestone from a different project
        can't be applied
        """

        pass

