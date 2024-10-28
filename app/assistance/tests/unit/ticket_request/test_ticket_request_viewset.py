from django.test import TestCase

from core.tests.abstract.test_ticket_viewset import Ticket, TicketViewSetPermissionsAPI


class TicketRequestPermissionsAPI(
    TicketViewSetPermissionsAPI,
    TestCase,
):

    ticket_type = 'request'

    ticket_type_enum = Ticket.TicketType.REQUEST
