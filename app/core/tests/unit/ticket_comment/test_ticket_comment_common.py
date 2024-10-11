import pytest
import unittest
import requests

from django.test import TestCase

from app.tests.abstract.models import ModelDisplay, ModelIndex

from core.models.ticket.ticket_comment import TicketComment



class TicketCommentCommon(
    TestCase
):

    model = TicketComment


    def test_ticket_field_type_opened_by(self):
        """Replies to comments only to occur on primary comment

        If a comment has a 'parent_id' set, ensure the comment can't be replied to
        """
        pass
