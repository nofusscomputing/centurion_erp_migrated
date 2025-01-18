import pytest

from django.contrib.auth.models import  User
from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models import Organization

from app.tests.abstract.mock_view import MockView

from core.serializers.ticket_related import (
    Ticket,
    RelatedTickets,
    RelatedTicketModelSerializer,
)



class RelatedTicketsValidationAPI(
    TestCase,
):

    model = RelatedTickets

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        2. Create an item
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        user = User.objects.create_user(username="test_user_view", password="password")

        self.user = user

        self.ticket_one = Ticket.objects.create(
            organization = self.organization,
            title = 'A ticket',
            description = 'the ticket body',
            ticket_type = Ticket.TicketType.REQUEST,
            opened_by = user,
            status = Ticket.TicketStatus.All.NEW.value
        )

        self.ticket_two = Ticket.objects.create(
            organization = self.organization,
            title = 'B ticket',
            description = 'the ticket body',
            ticket_type = Ticket.TicketType.REQUEST,
            opened_by = user,
            status = Ticket.TicketStatus.All.NEW.value
        )

        self.ticket_three = Ticket.objects.create(
            organization = self.organization,
            title = 'C ticket',
            description = 'the ticket body',
            ticket_type = Ticket.TicketType.REQUEST,
            opened_by = user,
            status = Ticket.TicketStatus.All.NEW.value
        )

        self.item = self.model.objects.create(
            organization = self.organization,
            from_ticket_id = self.ticket_one,
            to_ticket_id = self.ticket_two,
            how_related = RelatedTickets.Related.BLOCKS
        )




    def test_serializer_validation_create_valid(self):
        """Serializer Validation Check

        Ensure that a valid item is created and no validation error occurs
        """

        mock_view = MockView( user = self.user )

        serializer = RelatedTicketModelSerializer(
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data={
                'organization': self.organization.id,
                'from_ticket_id': self.ticket_one.id,
                'to_ticket_id': self.ticket_three.id,
                'how_related': RelatedTickets.Related.BLOCKS
            }
        )

        assert serializer.is_valid(raise_exception = True)



    def test_serializer_validation_add_existing_related_ticket(self):
        """Serializer Validation Check

        Ensure that if adding a duplicate linked ticket
        it raises a validation error
        """

        with pytest.raises(ValidationError) as err:

            mock_view = MockView( user = self.user )

            serializer = RelatedTicketModelSerializer(
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data={
                    'organization': self.organization.id,
                    'from_ticket_id': self.ticket_one.id,
                    'to_ticket_id': self.ticket_two.id,
                    'how_related': RelatedTickets.Related.BLOCKS
                }
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['to_ticket_id'][0] == 'duplicate_entry'



    def test_serializer_validation_add_existing_related_ticket_inverted(self):
        """Serializer Validation Check

        Ensure that if adding a duplicate linked ticket
        it raises a validation error
        """

        mock_view = MockView( user = self.user )

        with pytest.raises(ValidationError) as err:

            serializer = RelatedTicketModelSerializer(
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data={
                    'organization': self.organization.id,
                    'from_ticket_id': self.ticket_two.id,
                    'to_ticket_id': self.ticket_one.id,
                    'how_related': RelatedTickets.Related.BLOCKS
                }
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['to_ticket_id'][0] == 'duplicate_entry'



    def test_serializer_validation_add_blocked_by_self(self):
        """Serializer Validation Check

        Ensure that if adding itself as blocked by a validation
        error is thrown
        """

        mock_view = MockView( user = self.user )

        with pytest.raises(ValidationError) as err:

            serializer = RelatedTicketModelSerializer(
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data={
                    'organization': self.organization.id,
                    'from_ticket_id': self.ticket_two.id,
                    'to_ticket_id': self.ticket_two.id,
                    'how_related': RelatedTickets.Related.BLOCKED_BY
                }
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['to_ticket_id'][0] == 'self_not_related'



    def test_serializer_validation_add_blocks_self(self):
        """Serializer Validation Check

        Ensure that if adding itself as blocks a validation
        error is thrown
        """

        mock_view = MockView( user = self.user )

        with pytest.raises(ValidationError) as err:

            serializer = RelatedTicketModelSerializer(
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data={
                    'organization': self.organization.id,
                    'from_ticket_id': self.ticket_two.id,
                    'to_ticket_id': self.ticket_two.id,
                    'how_related': RelatedTickets.Related.BLOCKS
                }
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['to_ticket_id'][0] == 'self_not_related'



    def test_serializer_validation_add_related_self(self):
        """Serializer Validation Check

        Ensure that if adding itself as related a validation
        error is thrown
        """

        mock_view = MockView( user = self.user )

        with pytest.raises(ValidationError) as err:

            serializer = RelatedTicketModelSerializer(
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data={
                    'organization': self.organization.id,
                    'from_ticket_id': self.ticket_two.id,
                    'to_ticket_id': self.ticket_two.id,
                    'how_related': RelatedTickets.Related.RELATED
                }
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['to_ticket_id'][0] == 'self_not_related'
