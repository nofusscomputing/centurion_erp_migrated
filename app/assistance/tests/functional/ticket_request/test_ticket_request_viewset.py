from django.test import TestCase

from core.tests.abstract.test_ticket_viewset import Ticket, TicketViewSetBase, TicketViewSetPermissionsAPI, TicketViewSet



class ViewSetBase( TicketViewSetBase ):

    ticket_type = 'request'

    ticket_type_enum = Ticket.TicketType.REQUEST



class TicketRequestPermissionsAPI(
    ViewSetBase,
    TicketViewSetPermissionsAPI,
    TestCase,
):

    pass



class TicketRequestViewSet(
    TicketViewSet,
    ViewSetBase,
    TestCase,
):

    pass
