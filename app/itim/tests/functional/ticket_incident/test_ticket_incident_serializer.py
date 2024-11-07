import pytest

from django.test import TestCase

from core.models.ticket.ticket import Ticket
from core.models.ticket.ticket_category import TicketCategory

from itim.serializers.incident import (
    IncidentAddTicketModelSerializer,
    IncidentChangeTicketModelSerializer,
    IncidentImportTicketModelSerializer,
    IncidentTriageTicketModelSerializer
)

from project_management.models.projects import Project
from project_management.models.project_milestone import ProjectMilestone

from core.tests.abstract.test_ticket_serializer import TicketValidationAPI



class IncidentTicketValidationAPI(
    TicketValidationAPI,
    TestCase,
):

    add_serializer = IncidentAddTicketModelSerializer
    change_serializer = IncidentChangeTicketModelSerializer
    import_serializer = IncidentImportTicketModelSerializer
    triage_serializer = IncidentTriageTicketModelSerializer

    ticket_type = 'incident'

    ticket_type_enum = Ticket.TicketType.INCIDENT

    @classmethod
    def setUpTestData(self):

        super().setUpTestData()



    def test_serializer_add_field_remains_default_project(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation project should not be editable
        """

        assert self.created_ticket_add_serializer.project is None



    def test_serializer_triage_add_field_remains_default_project(self):
        """Ensure serializer allows edit

        For an ADD operation (triage serializer) project should be settable
        """

        assert self.created_ticket_triage_serializer.project.id == self.all_fields_data_triage['project']



    def test_serializer_triage_change_field_remains_default_project(self):
        """Ensure serializer allows edit

        For an Change operation (triage serializer) project should be settable
        """

        assert self.changed_ticket_triage_serializer.project.id == self.all_fields_data_triage_change['project']



    def test_serializer_import_add_field_editable_project(self):
        """Ensure serializer allows edit

        For an Add operation (import serializer) project should be settable
        """

        assert self.changed_ticket_triage_serializer.project.id == self.all_fields_data_import['project']

