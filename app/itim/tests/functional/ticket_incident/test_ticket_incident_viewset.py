from django.test import TestCase

from core.tests.abstract.test_ticket_viewset import Ticket, TicketViewSetBase, TicketViewSetPermissionsAPI, TicketViewSet
from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional, MetaDataNavigationEntriesFunctional


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



class TicketIncidentMetadata(
    ViewSetBase,
    MetadataAttributesFunctional,
    MetaDataNavigationEntriesFunctional,
    TestCase
):

    menu_id = 'itim'

    menu_entry_id = 'ticket_incident'
