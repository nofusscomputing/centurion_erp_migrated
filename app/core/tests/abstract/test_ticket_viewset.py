from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_permissions_viewset import APIPermissions
from api.tests.abstract.api_serializer_viewset import SerializersTestCases

from core.models.ticket.ticket import Ticket

from project_management.models.projects import Project

from settings.models.user_settings import UserSettings



class TicketViewSetBase:
    """ Test Cases common to ALL ticket types """

    model = Ticket

    app_namespace = 'v2'
    
    change_data = {'title': 'device'}

    delete_data = {}

    ticket_type: str = None
    """Name of ticket type in lower case, i.e. `request`"""

    ticket_type_enum:object = None
    """Ticket Type Enum for Ticket.TicketType"""


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a team
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        self.url_name = '_api_v2_ticket_' + self.ticket_type

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        different_organization = Organization.objects.create(name='test_different_organization')


        view_permissions = Permission.objects.get(
                codename = 'view_ticket_' + self.ticket_type,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        view_team = Team.objects.create(
            team_name = 'view_team',
            organization = organization,
        )

        view_team.permissions.set([view_permissions])



        add_permissions = Permission.objects.get(
                codename = 'add_ticket_' + self.ticket_type,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        add_team = Team.objects.create(
            team_name = 'add_team',
            organization = organization,
        )

        add_team.permissions.set([add_permissions])



        change_permissions = Permission.objects.get(
                codename = 'change_ticket_' + self.ticket_type,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        change_team = Team.objects.create(
            team_name = 'change_team',
            organization = organization,
        )

        change_team.permissions.set([change_permissions])



        delete_permissions = Permission.objects.get(
                codename = 'delete_ticket_' + self.ticket_type,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        delete_team = Team.objects.create(
            team_name = 'delete_team',
            organization = organization,
        )

        delete_team.permissions.set([delete_permissions])



        triage_permissions = Permission.objects.get(
                codename = 'triage_ticket_' + self.ticket_type,
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



        import_permissions = Permission.objects.get(
                codename = 'import_ticket_' + self.ticket_type,
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


        self.no_permissions_user = User.objects.create_user(username="test_no_permissions", password="password")


        self.view_user = User.objects.create_user(username="test_user_view", password="password")
        teamuser = TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )


        self.project = Project.objects.create(
            organization = self.organization,
            name = 'proj name'
        )


        self.item = self.model.objects.create(
            organization = self.organization,
            title = 'one',
            description = 'some text for body',
            opened_by = self.view_user,
            ticket_type = self.ticket_type_enum,
            status = Ticket.TicketStatus.All.NEW,
            project = self.project,
        )

        if self.ticket_type == 'project_task':

            self.url_kwargs = { 'project_id': self.project.id }

            self.url_view_kwargs = { 'project_id': self.project.id, 'pk': self.item.id}

        else:

            self.url_kwargs = {}

            self.url_view_kwargs = {'pk': self.item.id}


        self.add_data = {
            'title': 'team_post',
            'organization': self.organization.id,
            'description': 'article text',
            'ticket_type': int(self.ticket_type_enum),
            'status': int(Ticket.TicketStatus.All.NEW),
            'project': self.project.id,
        }


        self.add_user = User.objects.create_user(username="test_user_add", password="password")

        user_settings = UserSettings.objects.get(user=self.add_user)

        user_settings.default_organization = self.organization

        user_settings.save()


        teamuser = TeamUsers.objects.create(
            team = add_team,
            user = self.add_user
        )

        self.change_user = User.objects.create_user(username="test_user_change", password="password")
        teamuser = TeamUsers.objects.create(
            team = change_team,
            user = self.change_user
        )

        self.delete_user = User.objects.create_user(username="test_user_delete", password="password")
        teamuser = TeamUsers.objects.create(
            team = delete_team,
            user = self.delete_user
        )


        self.triage_user = User.objects.create_user(username="test_user_triage", password="password")
        teamuser = TeamUsers.objects.create(
            team = triage_team,
            user = self.triage_user
        )

        user_settings = UserSettings.objects.get(user=self.triage_user)

        user_settings.default_organization = self.organization

        user_settings.save()


        self.import_user = User.objects.create_user(username="test_user_import", password="password")
        teamuser = TeamUsers.objects.create(
            team = import_team,
            user = self.import_user
        )


        user_settings = UserSettings.objects.get(user=self.import_user)

        user_settings.default_organization = self.organization

        user_settings.save()



        self.different_organization_user = User.objects.create_user(username="test_different_organization_user", password="password")


        different_organization_team = Team.objects.create(
            team_name = 'different_organization_team',
            organization = different_organization,
        )

        different_organization_team.permissions.set([
            view_permissions,
            add_permissions,
            change_permissions,
            delete_permissions,
        ])

        TeamUsers.objects.create(
            team = different_organization_team,
            user = self.different_organization_user
        )



class TicketViewSetPermissionsAPI( TicketViewSetBase, APIPermissions ):


    def test_add_triage_user_denied(self):
        """ Check correct permission for add

        Attempt to add as triage user
        """

        client = Client()
        if self.url_kwargs:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')


        client.force_login(self.triage_user)
        response = client.post(url, data=self.add_data)

        assert response.status_code == 403



    def test_add_has_permission_import_user(self):
        """ Check correct permission for add 

        Attempt to add as import user who should have permission
        """

        client = Client()
        if self.url_kwargs:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')


        data = self.add_data.copy()

        data.update({
            'opened_by': self.import_user.id
        })

        client.force_login(self.import_user)
        response = client.post(url, data=data)

        assert response.status_code == 201



    def test_change_has_permission_triage_user(self):
        """ Check correct permission for change

        Make change with triage user who has change permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.triage_user)
        response = client.patch(url, data=self.change_data, content_type='application/json')

        assert response.status_code == 200



    def test_change_import_user_denied(self):
        """ Ensure permission view cant make change

        Attempt to make change as import user
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.import_user)
        response = client.patch(url, data=self.change_data, content_type='application/json')

        assert response.status_code == 403



    def test_delete_permission_triage_denied(self):
        """ Check correct permission for delete

        Attempt to delete as triage user
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.triage_user)
        response = client.delete(url, data=self.delete_data)

        assert response.status_code == 403



    def test_delete_permission_import_denied(self):
        """ Check correct permission for delete

        Attempt to delete as import user
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.import_user)
        response = client.delete(url, data=self.delete_data)

        assert response.status_code == 403



class TicketViewSet( TicketViewSetBase, SerializersTestCases ):


    @classmethod
    def setUpTestData(self):

        super().setUpTestData()


        if self.ticket_type == 'change':

            ticket_type_prefix = 'Change'

        elif self.ticket_type == 'incident':

            ticket_type_prefix = 'Incident'

        elif self.ticket_type == 'problem':

            ticket_type_prefix = 'Problem'

        elif self.ticket_type == 'project_task':

            ticket_type_prefix = 'ProjectTask'

        elif self.ticket_type == 'request':

            ticket_type_prefix = 'Request'


        self.ticket_type_prefix = ticket_type_prefix



    def test_add_has_permission_import_user(self):
        """ Check correct permission for add 

        Attempt to add as import user who should have permission
        """

        client = Client()
        if self.url_kwargs:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')


        data = self.add_data.copy()

        data.update({
            'opened_by': self.import_user.id
        })


        client.force_login(self.import_user)
        response = client.post(url, data=data)

        assert str(response.renderer_context['view'].get_serializer().__class__.__name__) == str(self.ticket_type_prefix + 'ImportTicketModelSerializer')



    def test_change_has_permission_triage_user(self):
        """ Check correct permission for change

        Make change with triage user who has change permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.triage_user)
        response = client.patch(url, data=self.change_data, content_type='application/json')

        assert str(response.renderer_context['view'].get_serializer().__class__.__name__) == str(self.ticket_type_prefix + 'TriageTicketModelSerializer')

