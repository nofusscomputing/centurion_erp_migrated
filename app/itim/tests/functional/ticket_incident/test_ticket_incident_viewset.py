from django.test import TestCase

from core.tests.abstract.test_ticket_viewset import Ticket, TicketViewSetBase, TicketViewSetPermissionsAPI, TicketViewSet


class ViewSetBase( TicketViewSetBase ):

    ticket_type = 'incident'

    ticket_type_enum = Ticket.TicketType.INCIDENT



class TicketIncidentPermissionsAPI(
    ViewSetBase,
    TicketViewSetPermissionsAPI,
    TestCase,
):

    pass



class TicketIncidentViewSet(
    TicketViewSet,
    ViewSetBase,
    TestCase,
):

    pass
