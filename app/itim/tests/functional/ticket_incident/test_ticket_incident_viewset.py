from django.test import TestCase

from core.tests.abstract.test_ticket_viewset import Ticket, TicketViewSetPermissionsAPI


class TicketIncidentPermissionsAPI(
    TicketViewSetPermissionsAPI,
    TestCase,
):

    ticket_type = 'incident'

    ticket_type_enum = Ticket.TicketType.INCIDENT
