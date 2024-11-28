from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from rest_framework.relations import Hyperlink

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_fields import APITenancyObject

from core.models.ticket.ticket_category import TicketCategory

from project_management.models.projects import Project
from project_management.models.project_milestone import ProjectMilestone


class TicketAPI(
    APITenancyObject
):
    """ Common Ticket API Field test cases

    Include these test cases in ALL ticket type field tests

    Args:
        APITenancyObject (class): Test Cases common to ALL API requests
    """

    model = None

    ticket_type: str = None
    """name of ticket in lowercase"""


    @classmethod
    def setUpTestData(self):
        """Setup Test

        This method should be `super` called from the inherited class

        1. Create an organization for user and item
        2. Create an item

        """

        self.organization = Organization.objects.create(name='test_org')


        self.project = Project.objects.create(
            organization = self.organization,
            name = 'a project',
        )

        self.project_milestone = ProjectMilestone.objects.create(
            organization = self.organization,
            name = 'a midlestone',
            project = self.project,
        )

        self.ticket_category = TicketCategory.objects.create(
            organization = self.organization,
            name = 'a ticket category',
        )


        view_permissions = Permission.objects.get(
            codename = 'view_ticket_' + self.ticket_type,
            content_type = ContentType.objects.get(
                app_label = self.model._meta.app_label,
                model = self.model._meta.model_name,
            )
        )

        self.view_team = Team.objects.create(
            team_name = 'view_team',
            organization = self.organization,
        )

        self.view_team.permissions.set([view_permissions])

        self.view_user = User.objects.create_user(username="test_user_view", password="password", is_superuser = True)
        teamuser = TeamUsers.objects.create(
            team = self.view_team,
            user = self.view_user
        )


    def test_api_field_exists_display_name(self):
        """ Test for existance of API Field

        This is a custom test case of a test with the same name.
        This test is required as this field does not exist

        display_name field must not exist
        """

        assert 'display_name' not in self.api_data


    def test_api_field_type_display_name(self):
        """ Test for type for API Field

        This is a custom test case of a test with the same name.
        This test is required as this field does not exist
        """

        assert True



    def test_api_field_exists_model_notes(self):
        """ Test for existance of API Field

        This is a custom test case of a test with the same name.
        This test is required as this field does not exist

        model_notes field must not exist
        """

        assert 'model_notes' not in self.api_data


    def test_api_field_type_model_notes(self):
        """ Test for type for API Field

        This is a custom test case of a test with the same name.
        This test is required as this field does not exist
        """

        assert True



    def test_api_field_exists_status_badge(self):
        """ Test for existance of API Field

        status_badge field must exist
        """

        assert 'status_badge' in self.api_data


    def test_api_field_type_status_badge(self):
        """ Test for type for API Field

        status_badge field must be int
        """

        assert type(self.api_data['status_badge']) is dict


    def test_api_field_exists_status_badge_icon(self):
        """ Test for existance of API Field

        status_badge.icon field must exist
        """

        assert 'icon' in self.api_data['status_badge']


    def test_api_field_type_status_badge_icon(self):
        """ Test for type for API Field

        status_badge.icon field must be dict
        """

        assert type(self.api_data['status_badge']['icon']) is dict


    def test_api_field_exists_status_badge_icon_name(self):
        """ Test for existance of API Field

        status_badge.icon.name field must exist
        """

        assert 'name' in self.api_data['status_badge']['icon']


    def test_api_field_type_status_badge_icon_name(self):
        """ Test for type for API Field

        status_badge.icon.name field must be str
        """

        assert type(self.api_data['status_badge']['icon']['name']) is str


    def test_api_field_exists_status_badge_icon_style(self):
        """ Test for existance of API Field

        status_badge.icon.style field must exist
        """

        assert 'style' in self.api_data['status_badge']['icon']


    def test_api_field_type_status_badge_icon_style(self):
        """ Test for type for API Field

        status_badge.icon.style field must be str
        """

        assert type(self.api_data['status_badge']['icon']['style']) is str



    def test_api_field_exists_status_badge_text(self):
        """ Test for existance of API Field

        status_badge.text field must exist
        """

        assert 'text' in self.api_data['status_badge']


    def test_api_field_type_status_badge_text(self):
        """ Test for type for API Field

        status_badge.text field must be str
        """

        assert type(self.api_data['status_badge']['text']) is str



    def test_api_field_exists_status_badge_text_style(self):
        """ Test for existance of API Field

        status_badge.text_style field must exist
        """

        assert 'text_style' in self.api_data['status_badge']


    def test_api_field_type_status_badge_text_style(self):
        """ Test for type for API Field

        status_badge.text_style field must be str
        """

        assert type(self.api_data['status_badge']['text_style']) is str



    def test_api_field_exists_title(self):
        """ Test for existance of API Field

        title field must exist
        """

        assert 'title' in self.api_data


    def test_api_field_type_title(self):
        """ Test for type for API Field

        title field must be str
        """

        assert type(self.api_data['title']) is str



    def test_api_field_exists_description(self):
        """ Test for existance of API Field

        description field must exist
        """

        assert 'description' in self.api_data


    def test_api_field_type_description(self):
        """ Test for type for API Field

        description field must be str
        """

        assert type(self.api_data['description']) is str



    def test_api_field_exists_ticket_type(self):
        """ Test for existance of API Field

        ticket_type field must exist
        """

        assert 'ticket_type' in self.api_data


    def test_api_field_type_description(self):
        """ Test for type for API Field

        ticket_type field must be int
        """

        assert type(self.api_data['ticket_type']) is int



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



    def test_api_field_exists_estimate(self):
        """ Test for existance of API Field

        estimate field must exist
        """

        assert 'estimate' in self.api_data


    def test_api_field_type_estimate(self):
        """ Test for type for API Field

        estimate field must be int
        """

        assert type(self.api_data['estimate']) is int



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



    def test_api_field_exists_urgency(self):
        """ Test for existance of API Field

        urgency field must exist
        """

        assert 'urgency' in self.api_data


    def test_api_field_type_urgency(self):
        """ Test for type for API Field

        urgency field must be int
        """

        assert type(self.api_data['urgency']) is int



    def test_api_field_exists_priority(self):
        """ Test for existance of API Field

        priority field must exist
        """

        assert 'priority' in self.api_data


    def test_api_field_type_urgency(self):
        """ Test for type for API Field

        priority field must be int
        """

        assert type(self.api_data['priority']) is int



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



    def test_api_field_exists_is_deleted(self):
        """ Test for existance of API Field

        is_deleted field must exist
        """

        assert 'is_deleted' in self.api_data


    def test_api_field_type_is_deleted(self):
        """ Test for type for API Field

        is_deleted field must be int
        """

        assert type(self.api_data['is_deleted']) is bool



    def test_api_field_exists_date_closed(self):
        """ Test for existance of API Field

        date_closed field must exist
        """

        assert 'date_closed' in self.api_data


    def test_api_field_type_date_closed(self):
        """ Test for type for API Field

        date_closed field must be int
        """

        assert type(self.api_data['date_closed']) is str



    def test_api_field_exists_project(self):
        """ Test for existance of API Field

        project field must exist
        """

        assert 'project' in self.api_data


    def test_api_field_type_project(self):
        """ Test for type for API Field

        project field must be int
        """

        assert type(self.api_data['project']) is dict


    def test_api_field_exists_project_id(self):
        """ Test for existance of API Field

        project.id field must exist
        """

        assert 'id' in self.api_data['project']


    def test_api_field_type_project_id(self):
        """ Test for type for API Field

        project.id field must be int
        """

        assert type(self.api_data['project']['id']) is int


    def test_api_field_exists_project_display_name(self):
        """ Test for existance of API Field

        project.display_name field must exist
        """

        assert 'display_name' in self.api_data['project']


    def test_api_field_type_project_display_name(self):
        """ Test for type for API Field

        project.display_name field must be str
        """

        assert type(self.api_data['project']['display_name']) is str


    def test_api_field_exists_project_url(self):
        """ Test for existance of API Field

        project.url field must exist
        """

        assert 'url' in self.api_data['project']


    def test_api_field_type_project_url(self):
        """ Test for type for API Field

        project.url field must be Hyperlink
        """

        assert type(self.api_data['project']['url']) is Hyperlink



    def test_api_field_exists_milestone(self):
        """ Test for existance of API Field

        milestone field must exist
        """

        assert 'milestone' in self.api_data


    def test_api_field_type_milestone(self):
        """ Test for type for API Field

        milestone field must be int
        """

        assert type(self.api_data['milestone']) is dict


    def test_api_field_exists_milestone_id(self):
        """ Test for existance of API Field

        milestone.id field must exist
        """

        assert 'id' in self.api_data['milestone']


    def test_api_field_type_milestone_id(self):
        """ Test for type for API Field

        milestone.id field must be int
        """

        assert type(self.api_data['milestone']['id']) is int


    def test_api_field_exists_milestone_display_name(self):
        """ Test for existance of API Field

        milestone.display_name field must exist
        """

        assert 'display_name' in self.api_data['milestone']


    def test_api_field_type_milestone_display_name(self):
        """ Test for type for API Field

        milestone.display_name field must be str
        """

        assert type(self.api_data['milestone']['display_name']) is str


    def test_api_field_exists_milestone_url(self):
        """ Test for existance of API Field

        milestone.url field must exist
        """

        assert 'url' in self.api_data['milestone']


    def test_api_field_type_milestone_url(self):
        """ Test for type for API Field

        milestone.url field must be str
        """

        assert type(self.api_data['milestone']['url']) is str



    def test_api_field_exists_assigned_teams(self):
        """ Test for existance of API Field

        assigned_teams field must exist
        """

        assert 'assigned_teams' in self.api_data


    def test_api_field_type_assigned_teams(self):
        """ Test for type for API Field

        assigned_teams field must be int
        """

        assert type(self.api_data['assigned_teams']) is list



    def test_api_field_exists_assigned_teams_id(self):
        """ Test for existance of API Field

        assigned_teams.id field must exist
        """

        assert 'id' in self.api_data['assigned_teams'][0]


    def test_api_field_type_assigned_teams_id(self):
        """ Test for type for API Field

        assigned_teams.id field must be int
        """

        assert type(self.api_data['assigned_teams'][0]['id']) is int


    def test_api_field_exists_assigned_teams_display_name(self):
        """ Test for existance of API Field

        assigned_teams.display_name field must exist
        """

        assert 'display_name' in self.api_data['assigned_teams'][0]


    def test_api_field_type_assigned_teams_display_name(self):
        """ Test for type for API Field

        assigned_teams.display_name field must be str
        """

        assert type(self.api_data['assigned_teams'][0]['display_name']) is str


    def test_api_field_exists_assigned_teams_url(self):
        """ Test for existance of API Field

        assigned_teams.url field must exist
        """

        assert 'url' in self.api_data['assigned_teams'][0]


    def test_api_field_type_assigned_teams_url(self):
        """ Test for type for API Field

        assigned_teams.url field must be str
        """

        assert type(self.api_data['assigned_teams'][0]['url']) is str



    def test_api_field_exists_assigned_users(self):
        """ Test for existance of API Field

        assigned_users field must exist
        """

        assert 'assigned_users' in self.api_data


    def test_api_field_type_assigned_users(self):
        """ Test for type for API Field

        assigned_users field must be int
        """

        assert type(self.api_data['assigned_users']) is list



    def test_api_field_exists_assigned_users_id(self):
        """ Test for existance of API Field

        assigned_users.id field must exist
        """

        assert 'id' in self.api_data['assigned_users'][0]


    def test_api_field_type_assigned_users_id(self):
        """ Test for type for API Field

        assigned_users.id field must be int
        """

        assert type(self.api_data['assigned_users'][0]['id']) is int


    def test_api_field_exists_assigned_users_display_name(self):
        """ Test for existance of API Field

        assigned_users.display_name field must exist
        """

        assert 'display_name' in self.api_data['assigned_users'][0]


    def test_api_field_type_assigned_users_display_name(self):
        """ Test for type for API Field

        assigned_users.display_name field must be str
        """

        assert type(self.api_data['assigned_users'][0]['display_name']) is str


    def test_api_field_exists_assigned_users_first_name(self):
        """ Test for existance of API Field

        assigned_users.first_name field must exist
        """

        assert 'first_name' in self.api_data['assigned_users'][0]


    def test_api_field_type_assigned_users_first_name(self):
        """ Test for type for API Field

        assigned_users.first_name field must be str
        """

        assert type(self.api_data['assigned_users'][0]['first_name']) is str


    def test_api_field_exists_assigned_users_last_name(self):
        """ Test for existance of API Field

        assigned_users.last_name field must exist
        """

        assert 'last_name' in self.api_data['assigned_users'][0]


    def test_api_field_type_assigned_users_last_name(self):
        """ Test for type for API Field

        assigned_users.last_name field must be str
        """

        assert type(self.api_data['assigned_users'][0]['last_name']) is str


    def test_api_field_exists_assigned_users_username(self):
        """ Test for existance of API Field

        assigned_users.username field must exist
        """

        assert 'username' in self.api_data['assigned_users'][0]


    def test_api_field_type_assigned_users_username(self):
        """ Test for type for API Field

        assigned_users.username field must be str
        """

        assert type(self.api_data['assigned_users'][0]['username']) is str


    def test_api_field_exists_assigned_users_is_active(self):
        """ Test for existance of API Field

        assigned_users.is_active field must exist
        """

        assert 'is_active' in self.api_data['assigned_users'][0]


    def test_api_field_type_assigned_users_is_active(self):
        """ Test for type for API Field

        assigned_users.is_active field must be bool
        """

        assert type(self.api_data['assigned_users'][0]['is_active']) is bool


    def test_api_field_exists_assigned_users_url(self):
        """ Test for existance of API Field

        assigned_users.url field must exist
        """

        assert 'url' in self.api_data['assigned_users'][0]


    def test_api_field_type_assigned_users_url(self):
        """ Test for type for API Field

        assigned_users.url field must be Hyperlink
        """

        assert type(self.api_data['assigned_users'][0]['url']) is Hyperlink



    def test_api_field_exists_subscribed_teams(self):
        """ Test for existance of API Field

        subscribed_teams field must exist
        """

        assert 'subscribed_teams' in self.api_data


    def test_api_field_type_subscribed_teams(self):
        """ Test for type for API Field

        subscribed_teams field must be int
        """

        assert type(self.api_data['subscribed_teams']) is list


    def test_api_field_exists_subscribed_teams_id(self):
        """ Test for existance of API Field

        subscribed_teams.id field must exist
        """

        assert 'id' in self.api_data['subscribed_teams'][0]


    def test_api_field_type_subscribed_teams_id(self):
        """ Test for type for API Field

        subscribed_teams.id field must be int
        """

        assert type(self.api_data['subscribed_teams'][0]['id']) is int


    def test_api_field_exists_subscribed_teams_display_name(self):
        """ Test for existance of API Field

        subscribed_teams.display_name field must exist
        """

        assert 'display_name' in self.api_data['subscribed_teams'][0]


    def test_api_field_type_subscribed_teams_display_name(self):
        """ Test for type for API Field

        subscribed_teams.display_name field must be str
        """

        assert type(self.api_data['subscribed_teams'][0]['display_name']) is str


    def test_api_field_exists_subscribed_teams_url(self):
        """ Test for existance of API Field

        subscribed_teams.url field must exist
        """

        assert 'url' in self.api_data['subscribed_teams'][0]


    def test_api_field_type_subscribed_teams_url(self):
        """ Test for type for API Field

        subscribed_teams.url field must be str
        """

        assert type(self.api_data['subscribed_teams'][0]['url']) is str



    def test_api_field_exists_subscribed_users(self):
        """ Test for existance of API Field

        subscribed_users field must exist
        """

        assert 'subscribed_users' in self.api_data


    def test_api_field_type_subscribed_users(self):
        """ Test for type for API Field

        subscribed_users field must be int
        """

        assert type(self.api_data['subscribed_users']) is list



    def test_api_field_exists_subscribed_users_id(self):
        """ Test for existance of API Field

        subscribed_users.id field must exist
        """

        assert 'id' in self.api_data['subscribed_users'][0]


    def test_api_field_type_subscribed_users_id(self):
        """ Test for type for API Field

        subscribed_users.id field must be int
        """

        assert type(self.api_data['subscribed_users'][0]['id']) is int


    def test_api_field_exists_subscribed_users_display_name(self):
        """ Test for existance of API Field

        subscribed_users.display_name field must exist
        """

        assert 'display_name' in self.api_data['subscribed_users'][0]


    def test_api_field_type_subscribed_users_display_name(self):
        """ Test for type for API Field

        subscribed_users.display_name field must be str
        """

        assert type(self.api_data['subscribed_users'][0]['display_name']) is str


    def test_api_field_exists_subscribed_users_first_name(self):
        """ Test for existance of API Field

        subscribed_users.first_name field must exist
        """

        assert 'first_name' in self.api_data['subscribed_users'][0]


    def test_api_field_type_subscribed_users_first_name(self):
        """ Test for type for API Field

        subscribed_users.first_name field must be str
        """

        assert type(self.api_data['subscribed_users'][0]['first_name']) is str


    def test_api_field_exists_subscribed_users_last_name(self):
        """ Test for existance of API Field

        subscribed_users.last_name field must exist
        """

        assert 'last_name' in self.api_data['subscribed_users'][0]


    def test_api_field_type_subscribed_users_last_name(self):
        """ Test for type for API Field

        subscribed_users.last_name field must be str
        """

        assert type(self.api_data['subscribed_users'][0]['last_name']) is str


    def test_api_field_exists_subscribed_users_username(self):
        """ Test for existance of API Field

        subscribed_users.username field must exist
        """

        assert 'username' in self.api_data['subscribed_users'][0]


    def test_api_field_type_subscribed_users_username(self):
        """ Test for type for API Field

        subscribed_users.username field must be str
        """

        assert type(self.api_data['subscribed_users'][0]['username']) is str


    def test_api_field_exists_subscribed_users_is_active(self):
        """ Test for existance of API Field

        subscribed_users.is_active field must exist
        """

        assert 'is_active' in self.api_data['subscribed_users'][0]


    def test_api_field_type_subscribed_users_is_active(self):
        """ Test for type for API Field

        subscribed_users.is_active field must be bool
        """

        assert type(self.api_data['subscribed_users'][0]['is_active']) is bool


    def test_api_field_exists_subscribed_users_url(self):
        """ Test for existance of API Field

        subscribed_users.url field must exist
        """

        assert 'url' in self.api_data['subscribed_users'][0]


    def test_api_field_type_subscribed_users_url(self):
        """ Test for type for API Field

        subscribed_users.url field must be Hyperlink
        """

        assert type(self.api_data['subscribed_users'][0]['url']) is Hyperlink



    def test_api_field_exists_opened_by(self):
        """ Test for existance of API Field

        opened_by field must exist
        """

        assert 'opened_by' in self.api_data


    def test_api_field_type_opened_by(self):
        """ Test for type for API Field

        opened_by field must be int
        """

        assert type(self.api_data['opened_by']) is dict


    def test_api_field_exists_opened_by_id(self):
        """ Test for existance of API Field

        opened_by.id field must exist
        """

        assert 'id' in self.api_data['opened_by']


    def test_api_field_type_opened_by_id(self):
        """ Test for type for API Field

        opened_by.id field must be int
        """

        assert type(self.api_data['opened_by']['id']) is int


    def test_api_field_exists_opened_by_display_name(self):
        """ Test for existance of API Field

        opened_by.display_name field must exist
        """

        assert 'display_name' in self.api_data['opened_by']


    def test_api_field_type_opened_by_display_name(self):
        """ Test for type for API Field

        opened_by.display_name field must be str
        """

        assert type(self.api_data['opened_by']['display_name']) is str


    def test_api_field_exists_opened_by_first_name(self):
        """ Test for existance of API Field

        opened_by.first_name field must exist
        """

        assert 'first_name' in self.api_data['opened_by']


    def test_api_field_type_opened_by_first_name(self):
        """ Test for type for API Field

        opened_by.first_name field must be str
        """

        assert type(self.api_data['opened_by']['first_name']) is str


    def test_api_field_exists_opened_by_last_name(self):
        """ Test for existance of API Field

        opened_by.last_name field must exist
        """

        assert 'last_name' in self.api_data['opened_by']


    def test_api_field_type_opened_by_last_name(self):
        """ Test for type for API Field

        opened_by.last_name field must be str
        """

        assert type(self.api_data['opened_by']['last_name']) is str


    def test_api_field_exists_opened_by_username(self):
        """ Test for existance of API Field

        opened_by.username field must exist
        """

        assert 'username' in self.api_data['opened_by']


    def test_api_field_type_opened_by_username(self):
        """ Test for type for API Field

        opened_by.username field must be str
        """

        assert type(self.api_data['opened_by']['username']) is str


    def test_api_field_exists_opened_by_is_active(self):
        """ Test for existance of API Field

        opened_by.is_active field must exist
        """

        assert 'is_active' in self.api_data['opened_by']


    def test_api_field_type_opened_by_is_active(self):
        """ Test for type for API Field

        opened_by.is_active field must be bool
        """

        assert type(self.api_data['opened_by']['is_active']) is bool


    def test_api_field_exists_opened_by_url(self):
        """ Test for existance of API Field

        opened_by.url field must exist
        """

        assert 'url' in self.api_data['opened_by']


    def test_api_field_type_opened_by_url(self):
        """ Test for type for API Field

        opened_by.url field must be Hyperlink
        """

        assert type(self.api_data['opened_by']['url']) is Hyperlink



    def test_api_field_exists__urls_comments(self):
        """ Test for existance of API Field

        _urls.comments field must exist
        """

        assert 'comments' in self.api_data['_urls']


    def test_api_field_type__urls_comments(self):
        """ Test for type for API Field

        _urls.comments field must be int
        """

        assert type(self.api_data['_urls']['comments']) is str



    def test_api_field_exists__urls_linked_items(self):
        """ Test for existance of API Field

        _urls.linked_items field must exist
        """

        assert 'linked_items' in self.api_data['_urls']


    def test_api_field_type__urls_linked_items(self):
        """ Test for type for API Field

        _urls.linked_items field must be int
        """

        assert type(self.api_data['_urls']['linked_items']) is str



    def test_api_field_exists__urls_related_tickets(self):
        """ Test for existance of API Field

        _urls.related_tickets field must exist
        """

        assert 'related_tickets' in self.api_data['_urls']


    def test_api_field_type__urls_related_tickets(self):
        """ Test for type for API Field

        _urls.related_tickets field must be int
        """

        assert type(self.api_data['_urls']['related_tickets']) is str
