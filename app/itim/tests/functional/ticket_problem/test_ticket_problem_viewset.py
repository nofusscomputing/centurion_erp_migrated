from django.test import TestCase

from core.tests.abstract.test_ticket_viewset import Ticket, TicketViewSetBase, TicketViewSetPermissionsAPI, TicketViewSet
from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional, MetaDataNavigationEntriesFunctional


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



class TicketProblemMetadata(
    ViewSetBase,
    MetadataAttributesFunctional,
    MetaDataNavigationEntriesFunctional,
    TestCase
):

    menu_id = 'itim'

    menu_entry_id = 'ticket_problem'
