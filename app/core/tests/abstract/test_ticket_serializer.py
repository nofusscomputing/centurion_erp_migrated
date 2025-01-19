import pytest

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from access.middleware.request import Tenancy
from access.models import Organization, Team, TeamUsers, Permission

from rest_framework.exceptions import ValidationError

from access.models import Organization

from core.models.ticket.ticket import Ticket
from core.models.ticket.ticket_category import TicketCategory


from project_management.models.projects import Project
from project_management.models.project_milestone import ProjectMilestone

from settings.models.app_settings import AppSettings



class MockView:

    _ticket_type_id: Ticket.TicketType = None

    _ticket_type: str = None

    action: str = None

    app_settings: AppSettings = None

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



class TicketValidationAPI(
    
):

    model = Ticket

    add_serializer = None
    change_serializer = None
    import_serializer = None
    triage_serializer = None

    ticket_type: str = None
    """Ticket type name in lowercase"""

    ticket_type_enum: Ticket.TicketType = None
    """Ticket type enum value"""

    add_data:dict = {}
    """data to add. Amend to this dict in each parent class"""


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        2. Create an item
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        organization_two = Organization.objects.create(name='test_org_two')

        self.organization_two = organization_two

        self.ticket_category = TicketCategory.objects.create(
            organization = self.organization,
            name = 'ticket category',
        )


        self.project = Project.objects.create(
            organization = self.organization,
            name = 'project name'
        )

        self.project_two = Project.objects.create(
            organization = self.organization,
            name = 'project name two'
        )

        self.project_milestone = ProjectMilestone.objects.create(
            organization = self.organization,
            name = 'project name',
            project = self.project
        )




        self.add_data.update({
            'organization': self.organization.id,
            'title': 'a ticket' + self.ticket_type,
            'description': 'ticket description',
            'project': self.project.id
        })


        self.add_user = User.objects.create_user(username="test_user_add", password="password")

        add_permissions = Permission.objects.get(
                codename = 'add_' + self.model._meta.model_name + '_' + self.ticket_type,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        self.add_team = Team.objects.create(
            team_name = 'add_team',
            organization = organization,
        )

        self.add_team.permissions.set([add_permissions])

        teamuser = TeamUsers.objects.create(
            team = self.add_team,
            user = self.add_user
        )


        self.change_user = User.objects.create_user(username="test_user_change", password="password")

        change_permissions = Permission.objects.get(
                codename = 'change_' + self.model._meta.model_name + '_' + self.ticket_type,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        self.change_team = Team.objects.create(
            team_name = 'change_team',
            organization = organization,
        )

        self.change_team.permissions.set([change_permissions])

        teamuser = TeamUsers.objects.create(
            team = self.change_team,
            user = self.change_user
        )


        self.triage_user = User.objects.create_user(username="test_user_triage", password="password")

        triage_permissions = Permission.objects.get(
                codename = 'triage_' + self.model._meta.model_name + '_' + self.ticket_type,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        triage_team = Team.objects.create(
            team_name = 'triage_team',
            organization = organization,
        )

        triage_team.permissions.set([triage_permissions])

        teamuser = TeamUsers.objects.create(
            team = triage_team,
            user = self.triage_user
        )


        self.import_user = User.objects.create_user(username="test_user_import", password="password")

        import_permissions = Permission.objects.get(
                codename = 'import_' + self.model._meta.model_name + '_' + self.ticket_type,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        import_team = Team.objects.create(
            team_name = 'import_team',
            organization = organization,
        )

        import_team.permissions.set([import_permissions])

        teamuser = TeamUsers.objects.create(
            team = import_team,
            user = self.import_user
        )


        self.ticket = Ticket.objects.create(
            organization=organization,
            title = 'ticket title',
            description = 'some text',
            opened_by = self.add_user,
            status = Ticket.TicketStatus.All.NEW,
            ticket_type = self.ticket_type_enum,
        )


        # use serializer with all fields to add an item (use save)
        # and check to ensure the fields not allowed, are not saved to db.

        self.all_fields_data: dict = {
            # Required Fields
            'organization': self.organization.id,
            'title': 'a ticket ' + self.ticket_type + ' all fields',
            'description': 'ticket description',

            # Remaining Fields
            'assigned_teams': [ self.add_team.id ],
            'assigned_users': [ self.add_user.id ],
            'category': self.ticket_category.id,
            'created': '2024-01-01T01:02:03Z',
            'modified': '2024-01-01T04:05:06Z',
            'status': int(Ticket.TicketStatus.All.CLOSED),
            'estimate': 1,
            'duration_ticket': 2,
            'urgency': int(Ticket.TicketUrgency.HIGH),
            'impact': int(Ticket.TicketImpact.MEDIUM),
            'priority': int(Ticket.TicketPriority.LOW),
            'external_ref': 3,
            'external_system': int(Ticket.Ticket_ExternalSystem.CUSTOM_1),
            'ticket_type': int(self.ticket_type_enum),
            'is_deleted': True,
            'date_closed': '2024-01-01T07:08:09Z',
            'planned_start_date': '2024-01-02T01:02:03Z',
            'planned_finish_date': '2024-01-02T02:03:04Z',
            'real_start_date': '2024-01-03T01:02:03Z',
            'real_finish_date': '2024-01-04T01:02:03Z',
            'opened_by': self.add_user.id,
            'organization': self.organization_two.id,
            'project': self.project.id,
            'milestone': self.project_milestone.id,
            'subscribed_teams': [ self.change_team.id ],
            'subscribed_users': [ self.change_user.id ]
        }



        #
        #  Add Serializer
        #


        mock_view = MockView( user = self.add_user )
        mock_view.action = 'create'
        mock_view._ticket_type_id = self.ticket_type_enum
        mock_view._ticket_type = self.ticket_type

        if self.ticket_type == 'project_task':

            mock_view.kwargs = {
                'project_id': self.project.id
            }

        # mock_request = MockRequest()
        # mock_request.user = self.add_user

        # mock_view.request = mock_request


        serializer = self.add_serializer(
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = self.all_fields_data
        )

        serializer.is_valid( raise_exception = True )

        serializer.save()

        self.created_ticket_add_serializer = serializer.instance



        #
        #  Change Serializer
        #


        self.ticket_for_change = Ticket.objects.create(
            organization=organization,
            title = 'ticket title for change serializer ' + self.ticket_type,
            description = 'some text',
            opened_by = self.add_user,
            status = Ticket.TicketStatus.All.NEW,
            ticket_type = self.ticket_type_enum,
            project = self.project_two
        )

        self.ticket_for_change.subscribed_users.add( self.add_user.id )

        self.all_fields_data_change = self.all_fields_data.copy()

        self.all_fields_data_change.update({
            'title': 'a change ticket ' + self.ticket_type + ' all fields',
        })

        del self.all_fields_data_change['organization']    # ToDo: Test seperatly


        mock_view = MockView( user = self.add_user)
        mock_view.action = 'partial_update'
        mock_view._ticket_type_id = self.ticket_type_enum
        mock_view._ticket_type = self.ticket_type

        if self.ticket_type == 'project_task':

            mock_view.kwargs = {
                'project_id': self.project.id
            }

        # mock_request = MockRequest()
        # mock_request.user = self.add_user

        # mock_view.request = mock_request


        serializer = self.change_serializer(
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = self.all_fields_data_change,
            instance = self.ticket_for_change,
            partial = True,
        )

        serializer.is_valid( raise_exception = True )

        serializer.save()

        self.created_ticket_change_serializer = serializer.instance


        #
        #  Triage Serializer Add New Ticket
        #


        self.all_fields_data_triage = self.all_fields_data.copy()

        self.all_fields_data_triage.update({
            'title': 'a triage ticket ' + self.ticket_type + ' all fields',
        })


        mock_view = MockView( user = self.add_user )
        mock_view.action = 'create'
        mock_view._ticket_type_id = self.ticket_type_enum
        mock_view._ticket_type = self.ticket_type

        if self.ticket_type == 'project_task':

            mock_view.kwargs = {
                'project_id': self.project.id
            }

        # mock_request = MockRequest()
        # mock_request.user = self.add_user

        # mock_view.request = mock_request


        serializer = self.triage_serializer(
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = self.all_fields_data_triage,
        )

        serializer.is_valid( raise_exception = True )

        serializer.save()

        self.created_ticket_triage_serializer = serializer.instance


        #
        #  Triage Serializer Change existing Ticket
        #


        self.ticket_for_triage_change = Ticket.objects.create(
            organization=organization,
            title = 'ticket title for change serializer ' + self.ticket_type,
            description = 'some text',
            opened_by = self.add_user,
            status = Ticket.TicketStatus.All.NEW,
            ticket_type = self.ticket_type_enum,
            project = self.project_two
        )

        self.ticket_for_triage_change.subscribed_users.add( self.add_user.id )

        self.all_fields_data_triage_change = self.all_fields_data.copy()

        self.all_fields_data_triage_change.update({
            'title': 'a triage change ticket ' + self.ticket_type + ' all fields',
        })

        del self.all_fields_data_triage_change['organization']    # ToDo: Test seperatly


        mock_view = MockView( user = self.add_user)
        mock_view.action = 'partial_update'
        mock_view._ticket_type_id = self.ticket_type_enum
        mock_view._ticket_type = self.ticket_type

        if self.ticket_type == 'project_task':

            mock_view.kwargs = {
                'project_id': self.project.id
            }

        # mock_request = MockRequest()
        # mock_request.user = self.add_user

        # mock_view.request = mock_request


        serializer = self.triage_serializer(
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = self.all_fields_data_triage_change,
            instance = self.ticket_for_triage_change,
            partial = True,
        )

        serializer.is_valid( raise_exception = True )

        serializer.save()

        self.changed_ticket_triage_serializer = serializer.instance




        #
        #  Import Serializer Add New Ticket
        #


        self.all_fields_data_import = self.all_fields_data.copy()

        self.all_fields_data_import.update({
            'title': 'a import ticket ' + self.ticket_type + ' all fields',
        })


        mock_view = MockView( user = self.add_user)
        mock_view.action = 'create'
        mock_view._ticket_type_id = self.ticket_type_enum
        mock_view._ticket_type = self.ticket_type

        if self.ticket_type == 'project_task':

            mock_view.kwargs = {
                'project_id': self.project.id
            }

        # mock_request = MockRequest()
        # mock_request.user = self.add_user

        # mock_view.request = mock_request


        serializer = self.import_serializer(
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = self.all_fields_data_import,
        )

        serializer.is_valid( raise_exception = True )

        serializer.save()

        self.created_ticket_import_serializer = serializer.instance




    def test_assigned_ticket_status_updates(self):

        ticket = Ticket.objects.create(
            organization=self.organization,
            title = 'ticket title test status',
            description = 'some text',
            opened_by = self.add_user,
            status = Ticket.TicketStatus.All.NEW,
            ticket_type = self.ticket_type_enum,
        )

        ticket.assigned_users.add(self.triage_user.id)

        assert ticket.status ==  Ticket.TicketStatus.All.ASSIGNED


    def test_serializer_validation_add_valid_ok(self):
        """Serializer Validation Check

        Ensure that valid data has no validation errors.
        """

        mock_view = MockView( user = self.add_user )
        mock_view.action = 'create'
        mock_view._ticket_type_id = self.ticket_type_enum
        mock_view._ticket_type = self.ticket_type

        if self.ticket_type == 'project_task':

            mock_view.kwargs = {
                'project_id': self.project.id
            }

        # mock_request = MockRequest()
        # mock_request.user = self.add_user

        # mock_view.request = mock_request


        serializer = self.add_serializer(
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = self.add_data
        )

        assert serializer.is_valid(raise_exception = True)




    def test_serializer_validation_change_valid_ok(self):
        """Serializer Validation Check

        Ensure that valid data has no validation errors.
        """

        mock_view = MockView( user = self.change_user)
        mock_view.action = 'partial_update'
        mock_view._ticket_type = self.ticket_type

        if self.ticket_type == 'project_task':

            mock_view.kwargs = {
                'project_id': self.project.id
            }

        # mock_request = MockRequest()
        # mock_request.user = self.change_user

        # mock_view.request = mock_request


        serializer = self.change_serializer(
            instance = self.ticket,
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = {
                'title': 'changed title'
            },
            partial = True,
        )

        assert serializer.is_valid(raise_exception = True)



    def test_serializer_validation_import_valid_ok(self):
        """Serializer Validation Check

        Ensure that valid data has no validation errors.
        """

        data = self.add_data.copy()

        data.update({
            'opened_by': self.add_user.id,
        })

        mock_view = MockView( user = self.import_user)
        mock_view.action = 'create'
        mock_view._ticket_type = self.ticket_type

        if self.ticket_type == 'project_task':

            mock_view.kwargs = {
                'project_id': self.project.id
            }

        # mock_request = MockRequest()
        # mock_request.user = self.import_user

        # mock_view.request = mock_request


        serializer = self.import_serializer(
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = data
        )

        assert serializer.is_valid(raise_exception = True)



    def test_serializer_validation_add_no_title(self):
        """Serializer Validation Check

        Ensure that if creating and a title
        is not provided a validation error occurs
        """

        data = self.add_data.copy()

        del data['title']

        mock_view = MockView( user = self.add_user)
        mock_view.action = 'create'
        mock_view._ticket_type = self.ticket_type

        if self.ticket_type == 'project_task':

            mock_view.kwargs = {
                'project_id': self.project.id
            }

        # mock_request = MockRequest()
        # mock_request.user = self.add_user

        # mock_view.request = mock_request


        with pytest.raises(ValidationError) as err:

            serializer = self.add_serializer(
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data = data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['title'][0] == 'required'



    def test_serializer_validation_add_no_description(self):
        """Serializer Validation Check

        Ensure that if creating and a description
        is not provided a validation error occurs
        """

        data = self.add_data.copy()

        del data['description']


        mock_view = MockView( user = self.add_user)
        mock_view.action = 'create'
        mock_view._ticket_type = self.ticket_type

        if self.ticket_type == 'project_task':

            mock_view.kwargs = {
                'project_id': self.project.id
            }

        # mock_request = MockRequest()
        # mock_request.user = self.add_user

        # mock_view.request = mock_request


        with pytest.raises(ValidationError) as err:

            serializer = self.add_serializer(
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data = data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['description'][0] == 'required'



    def test_serializer_validation_add_no_organization(self):
        """Serializer Validation Check

        Ensure that if creating and a organization
        is not provided a validation error occurs
        """

        data = self.add_data.copy()

        del data['organization']


        mock_view = MockView( user = self.add_user)
        mock_view.action = 'create'
        mock_view._ticket_type = self.ticket_type

        if self.ticket_type == 'project_task':

            mock_view.kwargs = {
                'project_id': self.project.id
            }

        # mock_request = MockRequest()
        # mock_request.user = self.add_user

        # mock_view.request = mock_request


        with pytest.raises(ValidationError) as err:

            serializer = self.add_serializer(
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data = data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['organization'][0] == 'required'




    def test_serializer_add_field_remains_default_assigned_teams(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation assigned_teams should not be editable
        """

        assert len(list(self.created_ticket_add_serializer.assigned_teams.all())) == 0



    def test_serializer_add_field_remains_default_assigned_users(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation assigned_users should not be editable
        """

        assert len(list(self.created_ticket_add_serializer.assigned_users.all())) == 0



    def test_serializer_add_field_remains_default_category(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation category should not be editable
        """

        assert self.created_ticket_add_serializer.category_id is None



    def test_serializer_add_field_remains_default_created(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation created should not be editable
        """

        assert (
            str(self.created_ticket_add_serializer.created) is not None
            and str(self.created_ticket_add_serializer.created) != self.all_fields_data['created']
        )



    def test_serializer_add_field_remains_default_modified(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation modified should not be editable
        """

        assert (
            str(self.created_ticket_add_serializer.modified) is not None
            and str(self.created_ticket_add_serializer.modified) != self.all_fields_data['modified']
        )



    def test_serializer_add_field_remains_default_status(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation status should not be editable
        """

        assert self.created_ticket_add_serializer.status == int(Ticket.TicketStatus.All.NEW)



    def test_serializer_add_field_remains_default_estimate(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation estimate should not be editable
        """

        assert self.created_ticket_add_serializer.estimate == 0



    def test_serializer_add_field_remains_default_duration_ticket(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation duration_ticket should not be editable
        """

        assert int(self.created_ticket_add_serializer.duration_ticket) == 0



    def test_serializer_add_field_remains_default_impact(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation impact should not be editable
        """

        assert self.created_ticket_add_serializer.impact == int(Ticket.TicketImpact.VERY_LOW)



    def test_serializer_add_field_remains_default_priority(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation priority should not be editable
        """

        assert self.created_ticket_add_serializer.priority == int(Ticket.TicketPriority.VERY_LOW)



    def test_serializer_add_field_remains_default_external_ref(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation external_ref should not be editable
        """

        assert self.created_ticket_add_serializer.external_ref is None



    def test_serializer_add_field_remains_default_external_system(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation external_system should not be editable
        """

        assert self.created_ticket_add_serializer.external_system is None



    def test_serializer_add_field_remains_default_ticket_type(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation ticket_type should not be editable
        """

        assert self.created_ticket_add_serializer.ticket_type == self.ticket_type_enum



    def test_serializer_add_field_remains_default_is_deleted(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation is_deleted should not be editable
        """

        assert self.created_ticket_add_serializer.is_deleted == False



    def test_serializer_add_field_remains_default_date_closed(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation date_closed should not be editable
        """

        assert self.created_ticket_add_serializer.date_closed is None



    def test_serializer_add_field_remains_default_planned_start_date(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation planned_start_date should not be editable
        """

        assert self.created_ticket_add_serializer.planned_start_date is None



    def test_serializer_add_field_remains_default_planned_finish_date(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation planned_finish_date should not be editable
        """

        assert self.created_ticket_add_serializer.planned_finish_date is None



    def test_serializer_add_field_remains_default_real_start_date(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation real_start_date should not be editable
        """

        assert self.created_ticket_add_serializer.real_start_date is None



    def test_serializer_add_field_remains_default_real_finish_date(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation real_finish_date should not be editable
        """

        assert self.created_ticket_add_serializer.real_finish_date is None



    def test_serializer_add_field_remains_default_opened_by(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation opened_by should not be editable
        """

        assert self.created_ticket_add_serializer.opened_by.id == self.add_user.id



    def test_serializer_add_field_remains_default_milestone(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation milestone should not be editable
        """

        assert self.created_ticket_add_serializer.milestone is None



    def test_serializer_add_field_remains_default_subscribed_teams(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation subscribed_teams should not be editable
        """

        assert len(list(self.created_ticket_add_serializer.subscribed_teams.all())) == 0



    def test_serializer_add_field_remains_default_subscribed_users(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation subscribed_users should not be editable
        """

        assert list(self.created_ticket_add_serializer.subscribed_users.all())[0].id == self.add_user.id



    def test_serializer_add_field_editable_urgency(self):
        """Ensure serializer allows edit

        For an ADD operation urgency should be settable
        """

        assert self.created_ticket_add_serializer.urgency == self.all_fields_data['urgency']



    def test_serializer_add_field_editable_organization(self):
        """Ensure serializer allows edit

        For an ADD operation organization should be settable
        """

        assert self.created_ticket_add_serializer.organization.id == self.all_fields_data['organization']











    def test_serializer_change_field_remains_default_assigned_teams(self):
        """Ensure serializer doesn't allow edit

        For an Change operation assigned_teams should not be editable
        """

        assert len(list(self.created_ticket_change_serializer.assigned_teams.all())) == 0



    def test_serializer_change_field_remains_default_assigned_users(self):
        """Ensure serializer doesn't allow edit

        For an Change operation assigned_users should not be editable
        """

        assert len(list(self.created_ticket_change_serializer.assigned_users.all())) == 0



    def test_serializer_change_field_remains_default_category(self):
        """Ensure serializer doesn't allow edit

        For an Change operation category should not be editable
        """

        assert self.created_ticket_change_serializer.category_id is None



    def test_serializer_change_field_remains_default_created(self):
        """Ensure serializer doesn't allow edit

        For an Change operation created should not be editable
        """

        assert (
            str(self.created_ticket_change_serializer.created) is not None
            and str(self.created_ticket_change_serializer.created) != self.all_fields_data_change['created']
        )



    def test_serializer_change_field_remains_default_modified(self):
        """Ensure serializer doesn't allow edit

        For an Change operation modified should not be editable
        """

        assert (
            str(self.created_ticket_change_serializer.modified) is not None
            and str(self.created_ticket_change_serializer.modified) != self.all_fields_data_change['modified']
        )



    def test_serializer_change_field_remains_default_status(self):
        """Ensure serializer doesn't allow edit

        For an Change operation status should not be editable
        """

        assert self.created_ticket_change_serializer.status == int(Ticket.TicketStatus.All.NEW)



    def test_serializer_change_field_remains_default_estimate(self):
        """Ensure serializer doesn't allow edit

        For an Change operation estimate should not be editable
        """

        assert self.created_ticket_change_serializer.estimate == 0



    def test_serializer_change_field_remains_default_duration_ticket(self):
        """Ensure serializer doesn't allow edit

        For an Change operation duration_ticket should not be editable
        """

        assert int(self.created_ticket_change_serializer.duration_ticket) == 0



    def test_serializer_change_field_remains_default_impact(self):
        """Ensure serializer doesn't allow edit

        For an Change operation impact should not be editable
        """

        assert self.created_ticket_change_serializer.impact == int(Ticket.TicketImpact.VERY_LOW)



    def test_serializer_change_field_remains_default_priority(self):
        """Ensure serializer doesn't allow edit

        For an Change operation priority should not be editable
        """

        assert self.created_ticket_change_serializer.priority == int(Ticket.TicketPriority.VERY_LOW)



    def test_serializer_change_field_remains_default_external_ref(self):
        """Ensure serializer doesn't allow edit

        For an Change operation external_ref should not be editable
        """

        assert self.created_ticket_change_serializer.external_ref is None



    def test_serializer_change_field_remains_default_external_system(self):
        """Ensure serializer doesn't allow edit

        For an Change operation external_system should not be editable
        """

        assert self.created_ticket_change_serializer.external_system is None



    def test_serializer_change_field_remains_default_ticket_type(self):
        """Ensure serializer doesn't allow edit

        For an Change operation ticket_type should not be editable
        """

        assert self.created_ticket_change_serializer.ticket_type == self.ticket_type_enum



    def test_serializer_change_field_remains_default_is_deleted(self):
        """Ensure serializer doesn't allow edit

        For an Change operation is_deleted should not be editable
        """

        assert self.created_ticket_change_serializer.is_deleted == False



    def test_serializer_change_field_remains_default_date_closed(self):
        """Ensure serializer doesn't allow edit

        For an Change operation date_closed should not be editable
        """

        assert self.created_ticket_change_serializer.date_closed is None



    def test_serializer_change_field_remains_default_planned_start_date(self):
        """Ensure serializer doesn't allow edit

        For an Change operation planned_start_date should not be editable
        """

        assert self.created_ticket_change_serializer.planned_start_date is None



    def test_serializer_change_field_remains_default_planned_finish_date(self):
        """Ensure serializer doesn't allow edit

        For an Change operation planned_finish_date should not be editable
        """

        assert self.created_ticket_change_serializer.planned_finish_date is None



    def test_serializer_change_field_remains_default_real_start_date(self):
        """Ensure serializer doesn't allow edit

        For an Change operation real_start_date should not be editable
        """

        assert self.created_ticket_change_serializer.real_start_date is None



    def test_serializer_change_field_remains_default_real_finish_date(self):
        """Ensure serializer doesn't allow edit

        For an Change operation real_finish_date should not be editable
        """

        assert self.created_ticket_change_serializer.real_finish_date is None



    def test_serializer_change_field_remains_default_opened_by(self):
        """Ensure serializer doesn't allow edit

        For an Change operation opened_by should not be editable
        """

        assert self.created_ticket_change_serializer.opened_by.id == self.add_user.id



    def test_serializer_change_field_remains_default_milestone(self):
        """Ensure serializer doesn't allow edit

        For an Change operation milestone should not be editable
        """

        assert self.created_ticket_change_serializer.milestone is None



    def test_serializer_change_field_remains_default_subscribed_teams(self):
        """Ensure serializer doesn't allow edit

        For an Change operation subscribed_teams should not be editable
        """

        assert len(list(self.created_ticket_change_serializer.subscribed_teams.all())) == 0



    def test_serializer_change_field_remains_default_subscribed_users(self):
        """Ensure serializer doesn't allow edit

        For an Change operation subscribed_users should not be editable
        """

        assert list(self.created_ticket_change_serializer.subscribed_users.all())[0].id == self.add_user.id



    def test_serializer_change_field_editable_urgency(self):
        """Ensure serializer allows edit

        For an Change operation urgency should be settable
        """

        assert self.created_ticket_change_serializer.urgency == self.all_fields_data_change['urgency']



    def test_serializer_change_field_remains_same_project(self):
        """Ensure serializer doesn't allow edit

        For an Change operation project should not be editable
        """

        assert self.created_ticket_change_serializer.project.id == self.ticket_for_change.project.id



    # def test_serializer_change_field_editable_organization(self):
    #     """Ensure serializer allows edit

    #     For an Change operation organization should be settable
    #     """

    #     assert self.created_ticket_change_serializer.organization.id == self.all_fields_data_change['organization']























    def test_serializer_triage_add_field_remains_default_created(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation created should not be editable
        """

        assert (
            str(self.created_ticket_triage_serializer.created) is not None
            and str(self.created_ticket_triage_serializer.created) != self.all_fields_data['created']
        )



    def test_serializer_triage_add_field_remains_default_modified(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation modified should not be editable
        """

        assert (
            str(self.created_ticket_triage_serializer.modified) is not None
            and str(self.created_ticket_triage_serializer.modified) != self.all_fields_data['modified']
        )



    def test_serializer_triage_add_field_remains_default_estimate(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation estimate should not be editable
        """

        assert self.created_ticket_triage_serializer.estimate == 0



    def test_serializer_triage_add_field_remains_default_duration_ticket(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation duration_ticket should not be editable
        """

        assert int(self.created_ticket_triage_serializer.duration_ticket) == 0



    def test_serializer_triage_add_field_remains_default_external_ref(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation external_ref should not be editable
        """

        assert self.created_ticket_triage_serializer.external_ref is None



    def test_serializer_triage_add_field_remains_default_external_system(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation external_system should not be editable
        """

        assert self.created_ticket_triage_serializer.external_system is None



    def test_serializer_triage_add_field_remains_default_ticket_type(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation ticket_type should not be editable
        """

        assert self.created_ticket_triage_serializer.ticket_type == self.ticket_type_enum



    def test_serializer_triage_add_field_remains_default_is_deleted(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation is_deleted should not be editable
        """

        assert self.created_ticket_triage_serializer.is_deleted == False



    def test_serializer_triage_add_field_remains_default_date_closed(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation date_closed should not be editable
        """

        assert self.created_ticket_triage_serializer.date_closed is None



    def test_serializer_triage_add_field_remains_default_planned_start_date(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation planned_start_date should not be editable
        """

        assert self.created_ticket_triage_serializer.planned_start_date is None



    def test_serializer_triage_add_field_remains_default_planned_finish_date(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation planned_finish_date should not be editable
        """

        assert self.created_ticket_triage_serializer.planned_finish_date is None



    def test_serializer_triage_add_field_remains_default_real_start_date(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation real_start_date should not be editable
        """

        assert self.created_ticket_triage_serializer.real_start_date is None



    def test_serializer_triage_add_field_remains_default_real_finish_date(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation real_finish_date should not be editable
        """

        assert self.created_ticket_triage_serializer.real_finish_date is None



    def test_serializer_triage_add_field_remains_default_opened_by(self):
        """Ensure serializer doesn't allow edit

        For an ADD operation opened_by should not be editable
        """

        assert self.created_ticket_triage_serializer.opened_by.id == self.add_user.id



    def test_serializer_triage_add_field_editable_urgency(self):
        """Ensure serializer allows edit

        For an ADD operation urgency should be settable
        """

        assert self.created_ticket_triage_serializer.urgency == self.all_fields_data['urgency']



    def test_serializer_triage_add_field_editable_organization(self):
        """Ensure serializer allows edit

        For an ADD operation organization should be settable
        """

        assert self.created_ticket_triage_serializer.organization.id == self.all_fields_data['organization']











    def test_serializer_triage_add_field_editable_assigned_teams(self):
        """Ensure serializer allows edit

        For an ADD operation (triage serializer) assigned_teams should be settable
        """

        assert list(self.created_ticket_triage_serializer.assigned_teams.all())[0].id == self.all_fields_data_triage['assigned_teams'][0]



    def test_serializer_triage_add_field_editable_assigned_users(self):
        """Ensure serializer allows edit

        For an ADD operation (triage serializer) assigned_users should be settable
        """

        assert list(self.created_ticket_triage_serializer.assigned_users.all())[0].id == self.all_fields_data_triage['assigned_users'][0]


    def test_serializer_triage_add_field_editable_category(self):
        """Ensure serializer allows edit

        For an ADD operation (triage serializer) category_id should be settable
        """

        assert self.created_ticket_triage_serializer.category_id == self.all_fields_data_triage['category']



    @pytest.mark.skip( reason = 'When a ticket is assigned the status changes. rewrite test to create ticket with serializer then edit field.')
    def test_serializer_triage_add_field_editable_status(self):
        """Ensure serializer allows edit

        For an ADD operation (triage serializer) status should be settable
        """

        assert int(self.created_ticket_triage_serializer.status) == int(self.all_fields_data_triage['status'])



    def test_serializer_triage_add_field_editable_impact(self):
        """Ensure serializer allows edit

        For an ADD operation (triage serializer) impact should be settable
        """

        assert self.created_ticket_triage_serializer.impact == self.all_fields_data_triage['impact']



    def test_serializer_triage_add_field_editable_priority(self):
        """Ensure serializer allows edit

        For an ADD operation (triage serializer) priority should be settable
        """

        assert self.created_ticket_triage_serializer.priority == self.all_fields_data_triage['priority']



    def test_serializer_triage_add_field_editable_milestone(self):
        """Ensure serializer allows edit

        For an ADD operation (triage serializer) milestone should be settable
        """

        assert self.created_ticket_triage_serializer.milestone.id == self.all_fields_data_triage['milestone']



    def test_serializer_triage_add_field_editable_subscribed_teams(self):
        """Ensure serializer allows edit

        For an ADD operation (triage serializer) subscribed_teams should be settable
        """

        assert list(self.created_ticket_triage_serializer.subscribed_teams.all())[0].id == self.all_fields_data_triage['subscribed_teams'][0]



    def test_serializer_triage_add_field_editable_subscribed_users(self):
        """Ensure serializer allows edit

        For an ADD operation (triage serializer) subscribed_users should be settable
        """

        assert (
            len(list(self.created_ticket_triage_serializer.subscribed_users.all())) == 2
            and list(self.created_ticket_triage_serializer.subscribed_users.all())[1].id == self.all_fields_data_triage['subscribed_users'][0]
        )





















    def test_serializer_triage_change_field_remains_default_created(self):
        """Ensure serializer doesn't allow edit

        For an Change operation (triage serializer) created should not be editable
        """

        assert (
            str(self.changed_ticket_triage_serializer.created) is not None
            and str(self.changed_ticket_triage_serializer.created) != self.all_fields_data['created']
        )



    def test_serializer_triage_change_field_remains_default_modified(self):
        """Ensure serializer doesn't allow edit

        For an Change operation (triage serializer) modified should not be editable
        """

        assert (
            str(self.changed_ticket_triage_serializer.modified) is not None
            and str(self.changed_ticket_triage_serializer.modified) != self.all_fields_data['modified']
        )



    def test_serializer_triage_change_field_remains_default_estimate(self):
        """Ensure serializer doesn't allow edit

        For an Change operation (triage serializer) estimate should not be editable
        """

        assert self.changed_ticket_triage_serializer.estimate == 0



    def test_serializer_triage_change_field_remains_default_duration_ticket(self):
        """Ensure serializer doesn't allow edit

        For an Change operation (triage serializer) duration_ticket should not be editable
        """

        assert int(self.changed_ticket_triage_serializer.duration_ticket) == 0



    def test_serializer_triage_change_field_remains_default_external_ref(self):
        """Ensure serializer doesn't allow edit

        For an Change operation (triage serializer) external_ref should not be editable
        """

        assert self.changed_ticket_triage_serializer.external_ref is None



    def test_serializer_triage_change_field_remains_default_external_system(self):
        """Ensure serializer doesn't allow edit

        For an Change operation (triage serializer) external_system should not be editable
        """

        assert self.changed_ticket_triage_serializer.external_system is None



    def test_serializer_triage_change_field_remains_default_ticket_type(self):
        """Ensure serializer doesn't allow edit

        For an Change operation (triage serializer) ticket_type should not be editable
        """

        assert self.changed_ticket_triage_serializer.ticket_type == self.ticket_type_enum



    def test_serializer_triage_change_field_remains_default_is_deleted(self):
        """Ensure serializer doesn't allow edit

        For an Change operation (triage serializer) is_deleted should not be editable
        """

        assert self.changed_ticket_triage_serializer.is_deleted == False



    def test_serializer_triage_change_field_remains_default_date_closed(self):
        """Ensure serializer doesn't allow edit

        For an Change operation (triage serializer) date_closed should not be editable
        """

        assert self.changed_ticket_triage_serializer.date_closed is None



    def test_serializer_triage_change_field_remains_default_planned_start_date(self):
        """Ensure serializer doesn't allow edit

        For an Change operation (triage serializer) planned_start_date should not be editable
        """

        assert self.changed_ticket_triage_serializer.planned_start_date is None



    def test_serializer_triage_change_field_remains_default_planned_finish_date(self):
        """Ensure serializer doesn't allow edit

        For an Change operation (triage serializer) planned_finish_date should not be editable
        """

        assert self.changed_ticket_triage_serializer.planned_finish_date is None



    def test_serializer_triage_change_field_remains_default_real_start_date(self):
        """Ensure serializer doesn't allow edit

        For an Change operation (triage serializer) real_start_date should not be editable
        """

        assert self.changed_ticket_triage_serializer.real_start_date is None



    def test_serializer_triage_change_field_remains_default_real_finish_date(self):
        """Ensure serializer doesn't allow edit

        For an Change operation (triage serializer) real_finish_date should not be editable
        """

        assert self.changed_ticket_triage_serializer.real_finish_date is None



    def test_serializer_triage_change_field_remains_default_opened_by(self):
        """Ensure serializer doesn't allow edit

        For an Change operation (triage serializer) opened_by should not be editable
        """

        assert self.changed_ticket_triage_serializer.opened_by.id == self.add_user.id



    def test_serializer_triage_change_field_editable_urgency(self):
        """Ensure serializer allows edit

        For an Change operation (triage serializer) urgency should be settable
        """

        assert self.changed_ticket_triage_serializer.urgency == self.all_fields_data['urgency']



    @pytest.mark.skip( reason = 'When a ticket is assigned the status changes. rewrite test to create ticket with serializer then edit field.')
    def test_serializer_triage_change_field_editable_organization(self):
        """Ensure serializer allows edit

        For an Change operation (triage serializer) organization should be settable
        """

        assert self.changed_ticket_triage_serializer.organization.id == self.all_fields_data['organization']











    def test_serializer_triage_change_field_editable_assigned_teams(self):
        """Ensure serializer allows edit

        For an Change operation (triage serializer) assigned_teams should be settable
        """

        assert list(self.changed_ticket_triage_serializer.assigned_teams.all())[0].id == self.all_fields_data_triage_change['assigned_teams'][0]



    def test_serializer_triage_change_field_editable_assigned_users(self):
        """Ensure serializer allows edit

        For an Change operation (triage serializer) assigned_users should be settable
        """

        assert list(self.changed_ticket_triage_serializer.assigned_users.all())[0].id == self.all_fields_data_triage_change['assigned_users'][0]


    def test_serializer_triage_change_field_editable_category(self):
        """Ensure serializer allows edit

        For an Change operation (triage serializer) category_id should be settable
        """

        assert self.changed_ticket_triage_serializer.category_id == self.all_fields_data_triage_change['category']



    @pytest.mark.skip( reason = 'When a ticket is assigned the status changes. rewrite test to create ticket with serializer then edit field.')
    def test_serializer_triage_change_field_editable_status(self):
        """Ensure serializer allows edit

        For an Change operation (triage serializer) status should be settable
        """

        assert int(self.changed_ticket_triage_serializer.status) == int(self.all_fields_data_triage_change['status'])



    def test_serializer_triage_change_field_editable_impact(self):
        """Ensure serializer allows edit

        For an Change operation (triage serializer) impact should be settable
        """

        assert self.changed_ticket_triage_serializer.impact == self.all_fields_data_triage_change['impact']



    def test_serializer_triage_change_field_editable_priority(self):
        """Ensure serializer allows edit

        For an Change operation (triage serializer) priority should be settable
        """

        assert self.changed_ticket_triage_serializer.priority == self.all_fields_data_triage_change['priority']



    def test_serializer_triage_change_field_editable_milestone(self):
        """Ensure serializer allows edit

        For an Change operation (triage serializer) milestone should be settable
        """

        assert self.changed_ticket_triage_serializer.milestone.id == self.all_fields_data_triage_change['milestone']



    def test_serializer_triage_change_field_editable_subscribed_teams(self):
        """Ensure serializer allows edit

        For an Change operation (triage serializer) subscribed_teams should be settable
        """

        assert list(self.changed_ticket_triage_serializer.subscribed_teams.all())[0].id == self.all_fields_data_triage_change['subscribed_teams'][0]



    def test_serializer_triage_change_field_editable_subscribed_users(self):
        """Ensure serializer allows edit

        For an Change operation (triage serializer) subscribed_users should be settable
        """

        assert (
            len(list(self.changed_ticket_triage_serializer.subscribed_users.all())) == 1
            and list(self.changed_ticket_triage_serializer.subscribed_users.all())[0].id == self.all_fields_data_triage_change['subscribed_users'][0]
        )











    def test_serializer_import_add_field_editable_created(self):
        """Ensure serializer allows edit

        For an Add operation (import serializer) created should be settable
        """

        assert str(self.created_ticket_import_serializer.created) == str(self.all_fields_data_import['created']).replace('T', ' ').replace('Z', '+00:00')


    @pytest.mark.skip( reason = 'any edit to object updates the field' )
    def test_serializer_import_add_field_editable_modified(self):
        """Ensure serializer allows edit

        For an Add operation (import serializer) modified should be settable
        """

        assert str(self.created_ticket_import_serializer.modified) == str(self.all_fields_data_import['modified']).replace('T', ' ').replace('Z', '+00:00')



    def test_serializer_import_add_field_editable_estimate(self):
        """Ensure serializer allows edit

        For an Add operation (import serializer) estimate should be settable
        """

        assert self.created_ticket_import_serializer.estimate == self.all_fields_data_import['estimate']



    # def test_serializer_import_add_field_editable_duration_ticket(self):
    #     """Ensure serializer allows edit

    #     For an Add operation (import serializer) duration_ticket should be settable
    #     """

    #     assert int(self.created_ticket_import_serializer.duration_ticket) == 'fixme not editable'


    def test_serializer_import_add_field_remains_default_duration_ticket(self):
        """Ensure serializer doesn't allow edit

        For an Add operation (import serializer) duration_ticket should not be editable
        """

        assert int(self.created_ticket_import_serializer.duration_ticket) == 0





    def test_serializer_import_add_field_editable_external_ref(self):
        """Ensure serializer allows edit

        For an Add operation (import serializer) external_ref should be settable
        """

        assert self.created_ticket_import_serializer.external_ref == self.all_fields_data_import['external_ref']



    def test_serializer_import_add_field_editable_external_system(self):
        """Ensure serializer allows edit

        For an Add operation (import serializer) external_system should be settable
        """

        assert self.created_ticket_import_serializer.external_system == self.all_fields_data_import['external_system']



    def test_serializer_import_add_field_editable_ticket_type(self):
        """Ensure serializer allows edit

        For an Add operation (import serializer) ticket_type should be settable
        """

        assert self.created_ticket_import_serializer.ticket_type == self.ticket_type_enum



    def test_serializer_import_add_field_editable_is_deleted(self):
        """Ensure serializer allows edit

        For an Add operation (import serializer) is_deleted should be settable
        """

        assert self.created_ticket_import_serializer.is_deleted == self.all_fields_data_import['is_deleted']



    def test_serializer_import_add_field_editable_date_closed(self):
        """Ensure serializer allows edit

        For an Add operation (import serializer) date_closed should be settable
        """

        assert str(self.created_ticket_import_serializer.date_closed) == str(self.all_fields_data_import['date_closed']).replace('T', ' ').replace('Z', '+00:00')



    def test_serializer_import_add_field_editable_planned_start_date(self):
        """Ensure serializer allows edit

        For an Add operation (import serializer) planned_start_date should be settable
        """

        assert str(self.created_ticket_import_serializer.planned_start_date) == str(self.all_fields_data_import['planned_start_date']).replace('T', ' ').replace('Z', '+00:00')



    def test_serializer_import_add_field_editable_planned_finish_date(self):
        """Ensure serializer allows edit

        For an Add operation (import serializer) planned_finish_date should be settable
        """

        assert str(self.created_ticket_import_serializer.planned_finish_date) == str(self.all_fields_data_import['planned_finish_date']).replace('T', ' ').replace('Z', '+00:00')



    def test_serializer_import_add_field_editable_real_start_date(self):
        """Ensure serializer allows edit

        For an Add operation (import serializer) real_start_date should be settable
        """

        assert str(self.created_ticket_import_serializer.real_start_date) == str(self.all_fields_data_import['real_start_date']).replace('T', ' ').replace('Z', '+00:00')



    def test_serializer_import_add_field_editable_real_finish_date(self):
        """Ensure serializer allows edit

        For an Add operation (import serializer) real_finish_date should be settable
        """

        assert str(self.created_ticket_import_serializer.real_finish_date) == str(self.all_fields_data_import['real_finish_date']).replace('T', ' ').replace('Z', '+00:00')



    def test_serializer_import_add_field_editable_opened_by(self):
        """Ensure serializer allows edit

        For an Add operation (import serializer) opened_by should be settable
        """

        assert self.created_ticket_import_serializer.opened_by.id == self.all_fields_data_import['opened_by']



    def test_serializer_import_add_field_editable_urgency(self):
        """Ensure serializer allows edit

        For an Add operation (import serializer) urgency should be settable
        """

        assert self.created_ticket_import_serializer.urgency == self.all_fields_data_import['urgency']



    def test_serializer_import_add_field_editable_organization(self):
        """Ensure serializer allows edit

        For an Add operation (import serializer) organization should be settable
        """

        assert self.created_ticket_import_serializer.organization.id == self.all_fields_data_import['organization']





    def test_serializer_import_add_field_editable_assigned_teams(self):
        """Ensure serializer allows edit

        For an Add operation (import serializer) assigned_teams should be settable
        """

        assert list(self.created_ticket_import_serializer.assigned_teams.all())[0].id == self.all_fields_data_triage['assigned_teams'][0]



    def test_serializer_import_add_field_editable_assigned_users(self):
        """Ensure serializer allows edit

        For an Add operation (import serializer) assigned_users should be settable
        """

        assert list(self.created_ticket_import_serializer.assigned_users.all())[0].id == self.all_fields_data_triage['assigned_users'][0]


    def test_serializer_import_add_field_editable_category(self):
        """Ensure serializer allows edit

        For an Add operation (import serializer) category_id should be settable
        """

        assert self.created_ticket_import_serializer.category_id == self.all_fields_data_triage['category']



    @pytest.mark.skip( reason = 'When a ticket is assigned the status changes. rewrite test to create ticket with serializer then edit field.')
    def test_serializer_import_add_field_editable_status(self):
        """Ensure serializer allows edit

        For an Add operation (import serializer) status should be settable
        """

        assert int(self.created_ticket_import_serializer.status) == int(self.all_fields_data_triage['status'])



    def test_serializer_import_add_field_editable_impact(self):
        """Ensure serializer allows edit

        For an Add operation (import serializer) impact should be settable
        """

        assert self.created_ticket_import_serializer.impact == self.all_fields_data_triage['impact']



    def test_serializer_import_add_field_editable_priority(self):
        """Ensure serializer allows edit

        For an Add operation (import serializer) priority should be settable
        """

        assert self.created_ticket_import_serializer.priority == self.all_fields_data_triage['priority']



    def test_serializer_import_add_field_editable_milestone(self):
        """Ensure serializer allows edit

        For an Add operation (import serializer) milestone should be settable
        """

        assert self.created_ticket_import_serializer.milestone.id == self.all_fields_data_triage['milestone']



    def test_serializer_import_add_field_editable_subscribed_teams(self):
        """Ensure serializer allows edit

        For an Add operation (import serializer) subscribed_teams should be settable
        """

        assert list(self.created_ticket_import_serializer.subscribed_teams.all())[0].id == self.all_fields_data_triage['subscribed_teams'][0]



    def test_serializer_import_add_field_editable_subscribed_users(self):
        """Ensure serializer allows edit

        For an Add operation (import serializer) subscribed_users should be settable
        """

        assert (
            len(list(self.created_ticket_import_serializer.subscribed_users.all())) == 2
            and list(self.created_ticket_import_serializer.subscribed_users.all())[1].id == self.all_fields_data_triage['subscribed_users'][0]
        )




    @pytest.mark.skip(reason='test to be written')
    def test_attribute_duration_ticket_value(self):
        """Attribute value test

        This aattribute calculates the ticket duration from
        it's comments. must return total time in seconds
        """

        pass



    @pytest.mark.skip(reason='test to be written')
    def test_field_milestone_no_project(self):
        """Field Value Test

        Ensure that a milestone can't be applied if no project
        has been selected
        """

        pass


    @pytest.mark.skip(reason='test to be written')
    def test_field_milestone_different_project(self):
        """Field Value Test

        Ensure that a milestone from a different project
        can't be applied
        """

        pass



