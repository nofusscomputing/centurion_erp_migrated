import pytest
import unittest
import requests

from django.test import TestCase

from app.tests.abstract.models import ModelDisplay, ModelIndex



class TicketCommon(
    TestCase
):


    @pytest.mark.skip(reason='to write')
    def test_ticket_field_type_opened_by(self):
        """Ensure field is of a certain type

        opened_by_field must be of type int
        """
        pass

    @pytest.mark.skip(reason='to write')
    def test_ticket_field_value_not_null_opened_by(self):
        """Ensure field is not null

        opened_by_field must be set and not null
        """
        pass


    @pytest.mark.skip(reason='to write')
    def test_ticket_field_value_auto_set_opened_by(self):
        """Ensure field is auto set within code

        opened_by_field must be set by code with non-tech user not being able to change
        """
        pass


    @pytest.mark.skip(reason='to write')
    def test_ticket_field_value_tech_set_opened_by(self):
        """Ensure field can be set by a technician

        opened_by_field can be set by a technician
        """
        pass



    @pytest.mark.skip(reason='to write')
    def test_ticket_type_fields(self):
        """Placeholder test

        following tests to be written:

        - only tech can change tech fields (same org)
        - non-tech cant see tech fields (same org) during creation
        - non-tech cant change tech fields (same org)
        - only tech can change tech fields (different org)
        - non-tech cant see tech fields (different org) during creation
        - non-tech cant change tech fields (different org)

        - itsm ticket has the itsm related fields
        - non-itsm ticket does not have any itsm related fields
        
        """
        pass
