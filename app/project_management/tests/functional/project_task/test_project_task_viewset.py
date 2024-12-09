from django.test import TestCase

from core.tests.abstract.test_ticket_viewset import Ticket, TicketViewSetBase, TicketViewSetPermissionsAPI, TicketViewSet
from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional


class ViewSetBase( TicketViewSetBase ):

    ticket_type = 'project_task'

    ticket_type_enum = Ticket.TicketType.PROJECT_TASK



class TicketProjectTaskPermissionsAPI(
    ViewSetBase,
    TicketViewSetPermissionsAPI,
    TestCase,
):

    pass



class TicketProjectTaskViewSet(
    TicketViewSet,
    ViewSetBase,
    TestCase,
):

    pass



class TicketProjectTaskMetadata(
    ViewSetBase,
    MetadataAttributesFunctional,
    TestCase
):

    pass
