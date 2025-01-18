import pytest

from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.exceptions import ValidationError

from access.middleware.auth import Tenancy
from access.models import Organization

from core.serializers.ticket_comment import (
    Ticket,
    TicketComment,

    TicketCommentITILFollowUpAddModelSerializer,
    TicketCommentITILSolutionAddModelSerializer,
    TicketCommentITILTaskAddModelSerializer,

    TicketCommentITILFollowUpTriageModelSerializer,
    TicketCommentITILSolutionTriageModelSerializer,
    TicketCommentITILTaskTriageModelSerializer,
)

from settings.models.app_settings import AppSettings


class MockView:

    action: str = None

    kwargs: dict = {}

    request = None


    def __init__(self, user: User):

        app_settings = AppSettings.objects.select_related('global_organization').get(
            owner_organization = None
        )

        self.request = MockRequest( user = user, app_settings = app_settings)



class MockRequest:

    tenancy: Tenancy = None

    user = None

    def __init__(self, user: User, app_settings):

        self.user = user

        self.app_settings = app_settings

        self.tenancy = Tenancy(
            user = user,
            app_settings = app_settings
        )



class TicketCommentValidationAPI:

    model = TicketComment

    serializer = None
    """Serializer to test"""

    serializer_data: dict = None
    """ Data to pass to the serialzer"""


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        2. Create an item
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.user = User.objects.create(
            username = 'user',
            password = 'password',
            is_superuser = True,
        )

        self.ticket = Ticket.objects.create(
            organization=organization,
            title = 'ticket title',
            description = 'some text',
            opened_by = self.user,
            status = Ticket.TicketStatus.All.NEW,
            ticket_type = Ticket.TicketType.REQUEST,
        )

        self.item = self.model.objects.create(
            organization=organization,
            body = 'some text',
            ticket = self.ticket
        )


        self.item_reply = self.model.objects.create(
            organization=organization,
            parent = self.item,
            body = 'some text for the discussion comment',
            ticket = self.ticket
        )


    def test_serializer_validation_add_valid_item(self):
        """Serializer Validation Check

        Ensure that a valid item it does not raise a validation error
        """

        mock_view = MockView( user = self.user )
        mock_view.action = 'create'

        # mock_request = MockRequest()
        # mock_request._user = self.user


        mock_view.kwargs: dict = {
            'ticket_id': int(self.ticket.id)
        }

        serializer = self.serializer(
            context = {
                'view': mock_view,
                'request': mock_view.request
            },
            data = self.serializer_data
        )

        assert serializer.is_valid(raise_exception = True)


    def test_serializer_validation_no_ticket(self):
        """Serializer Validation Check

        Ensure that no specified ticket raises a validation error
        """

        mock_view = MockView( user = self.user)
        mock_view.action = 'create'

        # mock_request = MockRequest()
        # mock_request._user = self.user

        serializer = self.serializer(
            context = {
                'view': mock_view,
                'request': mock_view.request
            },
            data = self.serializer_data
        )

        with pytest.raises(ValidationError) as err:

            serializer = self.serializer(
                context = {
                    'view': mock_view,
                    'request': mock_view.request
                },
                data = self.serializer_data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['ticket'] == 'required'


    def test_serializer_validation_no_body(self):
        """Serializer Validation Check

        Ensure that if no body specified a validation error is raised
        """

        mock_view = MockView( user = self.user )
        mock_view.action = 'create'
        mock_view.kwargs: dict = {
            'ticket_id': int(self.ticket.id)
        }


        # mock_request = MockRequest()
        # mock_request._user = self.user


        serializer_data:dict = self.serializer_data.copy()
        del serializer_data['body']


        with pytest.raises(ValidationError) as err:

            serializer = self.serializer(
                context = {
                    'view': mock_view,
                    'request': mock_view.request
                },
                data = serializer_data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['body'][0] == 'required'


    def test_serializer_validation_no_comment_type(self):
        """Serializer Validation Check

        Ensure that if no comment_type specified a validation error is raised
        """

        mock_view = MockView( user = self.user )
        mock_view.action = 'create'
        mock_view.kwargs: dict = {
            'ticket_id': int(self.ticket.id)
        }


        serializer_data:dict = self.serializer_data.copy()
        del serializer_data['comment_type']

        # mock_request = MockRequest()
        # mock_request._user = self.user


        with pytest.raises(ValidationError) as err:

            serializer = self.serializer(
                context = {
                    'view': mock_view,
                    'request': mock_view.request
                },
                data = serializer_data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['comment_type'][0] == 'required'


    def test_serializer_validation_can_reply_to_comment(self):
        """Serializer Validation Check

        Ensure that if the comment being replyed to is not a reply to
        a comment (a discussion), then a reply can be made.
        """

        mock_view = MockView( user = self.user)
        mock_view.action = 'create'
        mock_view.kwargs: dict = {
            'ticket_id': int(self.ticket.id),
        }

        # mock_request = MockRequest()
        # mock_request._user = self.user

        serializer_data:dict = self.serializer_data.copy()

        serializer_data.update({ 'body': 'reply to an un-replied comment'})

        serializer = self.serializer(
            context = {
                'view': mock_view,
                'request': mock_view.request
            },
            data = serializer_data
        )

        assert serializer.is_valid(raise_exception = True)


    def test_serializer_validation_no_reply_to_a_reply(self):
        """Serializer Validation Check

        Ensure that if the comment being replyed to is a reply to a
        discussion, that you can't reply to it.
        """

        mock_view = MockView( user = self.user )
        mock_view.action = 'create'
        mock_view.kwargs: dict = {
            'ticket_id': int(self.ticket.id),
            'parent_id': int(self.item_reply.id)
        }

        # mock_request = MockRequest()
        # mock_request._user = self.user

        serializer_data:dict = self.serializer_data.copy()

        serializer_data.update({ 'body': 'reply to a replied comment'})


        with pytest.raises(ValidationError) as err:

            serializer = self.serializer(
                context = {
                    'view': mock_view,
                    'request': mock_view.request
                },
                data = serializer_data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['parent'] == 'single_discussion_replies_only'



class TicketCommentITILFollowUpAddValidationAPI(
    TicketCommentValidationAPI,
    TestCase,
):

    serializer = TicketCommentITILFollowUpAddModelSerializer

    comment_type = TicketComment.CommentType.COMMENT


    @classmethod
    def setUpTestData(self):

        super().setUpTestData()

        self.serializer_data = {
            'organization': self.organization.id,
            'body': 'comment body',
            'comment_type': int(self.comment_type)
        }



class TicketCommentITILSolutionAddValidationAPI(
    TicketCommentValidationAPI,
    TestCase,
):

    serializer = TicketCommentITILSolutionAddModelSerializer

    comment_type = TicketComment.CommentType.SOLUTION


    @classmethod
    def setUpTestData(self):

        super().setUpTestData()

        self.serializer_data = {
            'organization': self.organization.id,
            'body': 'comment body',
            'comment_type': int(self.comment_type)
        }



class TicketCommentITILTaskAddValidationAPI(
    TicketCommentValidationAPI,
    TestCase,
):

    serializer = TicketCommentITILTaskAddModelSerializer

    comment_type = TicketComment.CommentType.TASK


    @classmethod
    def setUpTestData(self):

        super().setUpTestData()

        self.serializer_data = {
            'organization': self.organization.id,
            'ticket': self.ticket.id,
            'body': 'comment body',
            'comment_type': int(self.comment_type)
        }



class TicketCommentITILFollowUpTriageValidationAPI(
    TicketCommentValidationAPI,
    TestCase,
):

    serializer = TicketCommentITILFollowUpTriageModelSerializer

    comment_type = TicketComment.CommentType.COMMENT


    @classmethod
    def setUpTestData(self):

        super().setUpTestData()

        self.serializer_data = {
            'organization': self.organization.id,
            'body': 'comment body',
            'comment_type': int(self.comment_type)
        }



class TicketCommentITILSolutionTriageValidationAPI(
    TicketCommentValidationAPI,
    TestCase,
):

    serializer = TicketCommentITILSolutionTriageModelSerializer

    comment_type = TicketComment.CommentType.SOLUTION


    @classmethod
    def setUpTestData(self):

        super().setUpTestData()

        self.serializer_data = {
            'organization': self.organization.id,
            'body': 'comment body',
            'comment_type': int(self.comment_type)
        }



class TicketCommentITILTaskTriageValidationAPI(
    TicketCommentValidationAPI,
    TestCase,
):

    serializer = TicketCommentITILTaskTriageModelSerializer

    comment_type = TicketComment.CommentType.TASK


    @classmethod
    def setUpTestData(self):

        super().setUpTestData()

        self.serializer_data = {
            'organization': self.organization.id,
            'ticket': self.ticket.id,
            'body': 'comment body',
            'comment_type': int(self.comment_type)
        }
