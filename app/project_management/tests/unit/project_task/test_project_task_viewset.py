from django.test import TestCase

from core.tests.abstract.test_ticket_viewset import Ticket, TicketViewSetPermissionsAPI



class TicketProjectTaskPermissionsAPI(
    TicketViewSetPermissionsAPI,
    TestCase,
):

    ticket_type = 'project_task'

    ticket_type_enum = Ticket.TicketType.PROJECT_TASK
