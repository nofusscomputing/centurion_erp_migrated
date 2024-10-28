import pytest

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from rest_framework.relations import Hyperlink

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_fields import APITenancyObject

from core.models.ticket.ticket import Ticket
from core.models.ticket.ticket_comment import TicketComment, TicketCommentCategory



class TicketCommentAPI(
    TestCase,
    APITenancyObject
):

    model = TicketComment

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create an item

        """

        self.organization = Organization.objects.create(name='test_org')



        category = TicketCommentCategory.objects.create(
            organization=self.organization,
            name = 'cat'
        )


        view_permissions = Permission.objects.get(
                codename = 'view_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        view_team = Team.objects.create(
            team_name = 'view_team',
            organization = self.organization,
        )

        view_team.permissions.set([view_permissions])

        self.view_user = User.objects.create_user(username="test_user_view", password="password")
        teamuser = TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )


        self.ticket = Ticket.objects.create(
            organization=self.organization,
            title = 'A ticket',
            description = 'the ticket body',
            opened_by = self.view_user,
            ticket_type = int(Ticket.TicketType.REQUEST.value),
        )

        self.item = self.model.objects.create(
            organization = self.organization,
            body = 'one',
            ticket = self.ticket,
            category = category,
            user = self.view_user,
            external_ref = 1,
            external_system = Ticket.Ticket_ExternalSystem.CUSTOM_1,
            responsible_user = self.view_user,
            responsible_team = view_team,
            planned_start_date = '2024-01-01T01:02:03Z',
            planned_finish_date = '2024-01-02T01:02:03Z',
            real_start_date = '2024-01-03T01:02:03Z',
            real_finish_date = '2024-01-04T01:02:03Z',
            date_closed = '2024-01-05T01:02:03Z',
        )

        child_comment = self.model.objects.create(
            organization = self.organization,
            body = 'one',
            ticket = self.ticket,
            user = self.view_user,
            parent = self.item,
        )


        self.url_view_kwargs = {'ticket_id': self.ticket.id, 'pk': self.item.id}

        self.url_view_kwargs_child = {'ticket_id': self.ticket.id, 'parent_id': self.item.id, 'pk': child_comment.id}

        client = Client()
        url = reverse('v2:_api_v2_ticket_comments-detail', kwargs=self.url_view_kwargs)
        url_child = reverse('v2:_api_v2_ticket_comment_threads-detail', kwargs=self.url_view_kwargs_child)


        client.force_login(self.view_user)
        response = client.get(url)
        response_child = client.get(url_child)

        self.api_data = response.data
        self.api_data_child = response_child.data




    def test_api_field_exists_display_name(self):
        """ Test for existance of API Field

        This is a custom test of a test case with the same name.
        This model does not have this field.

        display_name field must not exist
        """

        assert 'display_name' not in self.api_data


    def test_api_field_type_display_name(self):
        """ Test for type for API Field

        This is a custom test of a test case with the same name.
        This model does not have this field.
        """

        assert True



    def test_api_field_exists_model_notes(self):
        """ Test for existance of API Field

        This is a custom test of a test case with the same name.
        This model does not have this field.

        model_notes field must not exist
        """

        assert 'model_notes' not in self.api_data


    def test_api_field_type_model_notes(self):
        """ Test for type for API Field

        This is a custom test of a test case with the same name.
        This model does not have this field.
        """

        assert True



    def test_api_field_exists_body(self):
        """ Test for existance of API Field

        body field must exist
        """

        assert 'body' in self.api_data


    def test_api_field_type_body(self):
        """ Test for type for API Field

        body field must be str
        """

        assert type(self.api_data['body']) is str



    def test_api_field_exists_parent(self):
        """ Test for existance of API Field

        parent field must exist
        """

        assert 'parent' in self.api_data_child


    def test_api_field_type_parent(self):
        """ Test for type for API Field

        parent field must be int
        """

        assert type(self.api_data_child['parent']) is int



    def test_api_field_exists_ticket(self):
        """ Test for existance of API Field

        ticket field must exist
        """

        assert 'ticket' in self.api_data


    def test_api_field_type_ticket(self):
        """ Test for type for API Field

        ticket field must be int
        """

        assert type(self.api_data['ticket']) is int



    def test_api_field_exists_external_ref(self):
        """ Test for existance of API Field

        external_ref field must exist
        """

        assert 'external_ref' in self.api_data


    def test_api_field_type_external_ref(self):
        """ Test for type for API Field

        external_ref field must be int
        """

        assert type(self.api_data['external_ref']) is int



    def test_api_field_exists_external_system(self):
        """ Test for existance of API Field

        external_system field must exist
        """

        assert 'external_system' in self.api_data


    def test_api_field_type_external_system(self):
        """ Test for type for API Field

        external_system field must be int
        """

        assert type(self.api_data['external_system']) is int



    def test_api_field_exists_comment_type(self):
        """ Test for existance of API Field

        comment_type field must exist
        """

        assert 'comment_type' in self.api_data


    def test_api_field_type_comment_type(self):
        """ Test for type for API Field

        comment_type field must be int
        """

        assert type(self.api_data['comment_type']) is int



    def test_api_field_exists_private(self):
        """ Test for existance of API Field

        private field must exist
        """

        assert 'private' in self.api_data


    def test_api_field_type_private(self):
        """ Test for type for API Field

        private field must be bool
        """

        assert type(self.api_data['private']) is bool



    def test_api_field_exists_duration(self):
        """ Test for existance of API Field

        duration field must exist
        """

        assert 'duration' in self.api_data


    def test_api_field_type_duration(self):
        """ Test for type for API Field

        duration field must be int
        """

        assert type(self.api_data['duration']) is int



    def test_api_field_exists_category(self):
        """ Test for existance of API Field

        category field must exist
        """

        assert 'category' in self.api_data


    def test_api_field_type_category(self):
        """ Test for type for API Field

        category field must be int
        """

        assert type(self.api_data['category']) is int



    def test_api_field_exists_template(self):
        """ Test for existance of API Field

        template field must exist
        """

        assert 'template' in self.api_data


    @pytest.mark.skip( reason = 'templating not yet implemented' )
    def test_api_field_type_template(self):
        """ Test for type for API Field

        template field must be int
        """

        assert type(self.api_data['template']) is int



    def test_api_field_exists_is_template(self):
        """ Test for existance of API Field

        is_template field must exist
        """

        assert 'is_template' in self.api_data


    def test_api_field_type_is_template(self):
        """ Test for type for API Field

        is_template field must be bool
        """

        assert type(self.api_data['is_template']) is bool



    def test_api_field_exists_source(self):
        """ Test for existance of API Field

        source field must exist
        """

        assert 'source' in self.api_data


    def test_api_field_type_source(self):
        """ Test for type for API Field

        source field must be int
        """

        assert type(self.api_data['source']) is int



    def test_api_field_exists_status(self):
        """ Test for existance of API Field

        status field must exist
        """

        assert 'status' in self.api_data


    def test_api_field_type_status(self):
        """ Test for type for API Field

        status field must be int
        """

        assert type(self.api_data['status']) is int



    def test_api_field_exists_responsible_user(self):
        """ Test for existance of API Field

        responsible_user field must exist
        """

        assert 'responsible_user' in self.api_data


    def test_api_field_type_responsible_user(self):
        """ Test for type for API Field

        responsible_user field must be dict
        """

        assert type(self.api_data['responsible_user']) is dict



    def test_api_field_exists_responsible_user_id(self):
        """ Test for existance of API Field

        responsible_user.id field must exist
        """

        assert 'id' in self.api_data['responsible_user']


    def test_api_field_type_responsible_user_id(self):
        """ Test for type for API Field

        responsible_user.id field must be int
        """

        assert type(self.api_data['responsible_user']['id']) is int


    def test_api_field_exists_responsible_user_display_name(self):
        """ Test for existance of API Field

        responsible_user.display_name field must exist
        """

        assert 'display_name' in self.api_data['responsible_user']


    def test_api_field_type_responsible_user_display_name(self):
        """ Test for type for API Field

        responsible_user.display_name field must be str
        """

        assert type(self.api_data['responsible_user']['display_name']) is str


    def test_api_field_exists_responsible_user_first_name(self):
        """ Test for existance of API Field

        responsible_user.first_name field must exist
        """

        assert 'first_name' in self.api_data['responsible_user']


    def test_api_field_type_responsible_user_first_name(self):
        """ Test for type for API Field

        responsible_user.first_name field must be str
        """

        assert type(self.api_data['responsible_user']['first_name']) is str


    def test_api_field_exists_responsible_user_last_name(self):
        """ Test for existance of API Field

        responsible_user.last_name field must exist
        """

        assert 'last_name' in self.api_data['responsible_user']


    def test_api_field_type_responsible_user_last_name(self):
        """ Test for type for API Field

        responsible_user.last_name field must be str
        """

        assert type(self.api_data['responsible_user']['last_name']) is str


    def test_api_field_exists_responsible_user_username(self):
        """ Test for existance of API Field

        responsible_user.username field must exist
        """

        assert 'username' in self.api_data['responsible_user']


    def test_api_field_type_responsible_user_username(self):
        """ Test for type for API Field

        responsible_user.username field must be str
        """

        assert type(self.api_data['responsible_user']['username']) is str


    def test_api_field_exists_responsible_user_is_active(self):
        """ Test for existance of API Field

        responsible_user.is_active field must exist
        """

        assert 'is_active' in self.api_data['responsible_user']


    def test_api_field_type_responsible_user_is_active(self):
        """ Test for type for API Field

        responsible_user.is_active field must be bool
        """

        assert type(self.api_data['responsible_user']['is_active']) is bool


    def test_api_field_exists_responsible_user_url(self):
        """ Test for existance of API Field

        responsible_user.url field must exist
        """

        assert 'url' in self.api_data['responsible_user']


    def test_api_field_type_responsible_user_url(self):
        """ Test for type for API Field

        responsible_user.url field must be Hyperlink
        """

        assert type(self.api_data['responsible_user']['url']) is Hyperlink



    def test_api_field_exists_responsible_team(self):
        """ Test for existance of API Field

        responsible_team field must exist
        """

        assert 'responsible_team' in self.api_data


    def test_api_field_type_responsible_team(self):
        """ Test for type for API Field

        responsible_team field must be dict
        """

        assert type(self.api_data['responsible_team']) is dict



    def test_api_field_exists_responsible_team_id(self):
        """ Test for existance of API Field

        responsible_team.id field must exist
        """

        assert 'id' in self.api_data['responsible_team']


    def test_api_field_type_responsible_team_id(self):
        """ Test for type for API Field

        responsible_team.id field must be int
        """

        assert type(self.api_data['responsible_team']['id']) is int


    def test_api_field_exists_responsible_team_display_name(self):
        """ Test for existance of API Field

        responsible_team.display_name field must exist
        """

        assert 'display_name' in self.api_data['responsible_team']


    def test_api_field_type_responsible_team_display_name(self):
        """ Test for type for API Field

        responsible_team.display_name field must be str
        """

        assert type(self.api_data['responsible_team']['display_name']) is str


    def test_api_field_exists_responsible_team_url(self):
        """ Test for existance of API Field

        responsible_team.url field must exist
        """

        assert 'url' in self.api_data['responsible_team']


    def test_api_field_type_responsible_team_url(self):
        """ Test for type for API Field

        responsible_team.url field must be str
        """

        assert type(self.api_data['responsible_team']['url']) is str



    def test_api_field_exists_user(self):
        """ Test for existance of API Field

        user field must exist
        """

        assert 'user' in self.api_data


    def test_api_field_type_user(self):
        """ Test for type for API Field

        user field must be dict
        """

        assert type(self.api_data['user']) is dict



    def test_api_field_exists_user_id(self):
        """ Test for existance of API Field

        user.id field must exist
        """

        assert 'id' in self.api_data['user']


    def test_api_field_type_user_id(self):
        """ Test for type for API Field

        user.id field must be int
        """

        assert type(self.api_data['user']['id']) is int


    def test_api_field_exists_user_display_name(self):
        """ Test for existance of API Field

        user.display_name field must exist
        """

        assert 'display_name' in self.api_data['user']


    def test_api_field_type_user_display_name(self):
        """ Test for type for API Field

        user.display_name field must be str
        """

        assert type(self.api_data['user']['display_name']) is str


    def test_api_field_exists_user_first_name(self):
        """ Test for existance of API Field

        user.first_name field must exist
        """

        assert 'first_name' in self.api_data['user']


    def test_api_field_type_user_first_name(self):
        """ Test for type for API Field

        user.first_name field must be str
        """

        assert type(self.api_data['user']['first_name']) is str


    def test_api_field_exists_user_last_name(self):
        """ Test for existance of API Field

        user.last_name field must exist
        """

        assert 'last_name' in self.api_data['user']


    def test_api_field_type_user_last_name(self):
        """ Test for type for API Field

        user.last_name field must be str
        """

        assert type(self.api_data['user']['last_name']) is str


    def test_api_field_exists_user_username(self):
        """ Test for existance of API Field

        user.username field must exist
        """

        assert 'username' in self.api_data['user']


    def test_api_field_type_user_username(self):
        """ Test for type for API Field

        user.username field must be str
        """

        assert type(self.api_data['user']['username']) is str


    def test_api_field_exists_user_is_active(self):
        """ Test for existance of API Field

        user.is_active field must exist
        """

        assert 'is_active' in self.api_data['user']


    def test_api_field_type_user_is_active(self):
        """ Test for type for API Field

        user.is_active field must be bool
        """

        assert type(self.api_data['user']['is_active']) is bool


    def test_api_field_exists_user_url(self):
        """ Test for existance of API Field

        user.url field must exist
        """

        assert 'url' in self.api_data['user']


    def test_api_field_type_user_url(self):
        """ Test for type for API Field

        user.url field must be Hyperlink
        """

        assert type(self.api_data['user']['url']) is Hyperlink



    def test_api_field_exists_planned_start_date(self):
        """ Test for existance of API Field

        planned_start_date field must exist
        """

        assert 'planned_start_date' in self.api_data


    def test_api_field_type_planned_start_date(self):
        """ Test for type for API Field

        planned_start_date field must be str
        """

        assert type(self.api_data['planned_start_date']) is str



    def test_api_field_exists_planned_finish_date(self):
        """ Test for existance of API Field

        planned_finish_date field must exist
        """

        assert 'planned_finish_date' in self.api_data


    def test_api_field_type_planned_finish_date(self):
        """ Test for type for API Field

        planned_finish_date field must be str
        """

        assert type(self.api_data['planned_finish_date']) is str



    def test_api_field_exists_real_start_date(self):
        """ Test for existance of API Field

        real_start_date field must exist
        """

        assert 'real_start_date' in self.api_data


    def test_api_field_type_real_start_date(self):
        """ Test for type for API Field

        real_start_date field must be str
        """

        assert type(self.api_data['real_start_date']) is str



    def test_api_field_exists_real_finish_date(self):
        """ Test for existance of API Field

        real_finish_date field must exist
        """

        assert 'real_finish_date' in self.api_data


    def test_api_field_type_real_finish_date(self):
        """ Test for type for API Field

        real_finish_date field must be str
        """

        assert type(self.api_data['real_finish_date']) is str



    def test_api_field_exists_date_closed(self):
        """ Test for existance of API Field

        date_closed field must exist
        """

        assert 'date_closed' in self.api_data


    def test_api_field_type_date_closed(self):
        """ Test for type for API Field

        date_closed field must be str
        """

        assert type(self.api_data['date_closed']) is str

