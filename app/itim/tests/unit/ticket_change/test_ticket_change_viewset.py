from django.test import TestCase

from core.tests.abstract.test_ticket_viewset import Ticket, TicketViewSetPermissionsAPI


class TicketChangePermissionsAPI(
    TicketViewSetPermissionsAPI,
    TestCase,
):

    ticket_type = 'change'

    ticket_type_enum = Ticket.TicketType.CHANGE
