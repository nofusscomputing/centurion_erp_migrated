from django.test import TestCase

from core.tests.abstract.test_ticket_viewset import Ticket, TicketViewSetPermissionsAPI


class TicketProblemPermissionsAPI(
    TicketViewSetPermissionsAPI,
    TestCase,
):

    ticket_type = 'problem'

    ticket_type_enum = Ticket.TicketType.PROBLEM
