from django.test import TestCase

from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional, MetaDataNavigationEntriesFunctional

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



class TicketRequestMetadata(
    ViewSetBase,
    MetadataAttributesFunctional,
    MetaDataNavigationEntriesFunctional,
    TestCase
):

    menu_id = 'assistance'

    menu_entry_id = 'request'
