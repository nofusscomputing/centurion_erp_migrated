from django.test import TestCase

from core.tests.abstract.test_ticket_viewset import Ticket, TicketViewSetBase, TicketViewSetPermissionsAPI, TicketViewSet


class ViewSetBase( TicketViewSetBase ):

    ticket_type = 'change'

    ticket_type_enum = Ticket.TicketType.CHANGE



class TicketChangePermissionsAPI(
    ViewSetBase,
    TicketViewSetPermissionsAPI,
    TestCase,
):

    pass



class TicketChangeViewSet(
    TicketViewSet,
    ViewSetBase,
    TestCase,
):

    pass
