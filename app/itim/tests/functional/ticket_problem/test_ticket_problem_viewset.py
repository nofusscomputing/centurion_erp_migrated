from django.test import TestCase

from core.tests.abstract.test_ticket_viewset import Ticket, TicketViewSetBase, TicketViewSetPermissionsAPI, TicketViewSet


class ViewSetBase( TicketViewSetBase ):

    ticket_type = 'problem'

    ticket_type_enum = Ticket.TicketType.PROBLEM



class TicketProblemPermissionsAPI(
    ViewSetBase,
    TicketViewSetPermissionsAPI,
    TestCase,
):

    pass



class TicketProblemViewSet(
    TicketViewSet,
    ViewSetBase,
    TestCase,
):

    pass
