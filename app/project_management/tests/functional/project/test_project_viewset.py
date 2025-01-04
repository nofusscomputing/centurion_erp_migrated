import pytest

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_permissions_viewset import APIPermissions
from api.tests.abstract.api_serializer_viewset import SerializersTestCases
from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional, MetaDataNavigationEntriesFunctional

from project_management.models.projects import Project

from settings.models.app_settings import AppSettings



class ViewSetBase:

    model = Project

    app_namespace = 'v2'
    
    url_name = '_api_v2_project'

    change_data = {'name': 'device-change'}

    delete_data = {}

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a team
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        different_organization = Organization.objects.create(name='test_different_organization')

        self.different_organization = different_organization





        self.global_organization = Organization.objects.create(
            name = 'test_global_organization'
        )

        self.global_org_item = self.model.objects.create(
            organization = self.global_organization,
            name = 'global_item'
        )

        app_settings = AppSettings.objects.get(
            owner_organization = None
        )

        app_settings.global_organization = self.global_organization

        app_settings.save()






        view_permissions = Permission.objects.get(
                codename = 'view_' + self.model._meta.model_name,
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
                codename = 'add_' + self.model._meta.model_name,
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
                codename = 'change_' + self.model._meta.model_name,
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
                codename = 'delete_' + self.model._meta.model_name,
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


        import_permissions = Permission.objects.get(
                codename = 'import_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        import_team = Team.objects.create(
            team_name = 'import_team',
            organization = organization,
        )

        import_team.permissions.set( [ import_permissions, add_permissions ] )


        self.import_user = User.objects.create_user(username="test_user_import", password="password")
        teamuser = TeamUsers.objects.create(
            team = import_team,
            user = self.import_user
        )


        self.no_permissions_user = User.objects.create_user(username="test_no_permissions", password="password")


        self.view_user = User.objects.create_user(username="test_user_view", password="password")
        teamuser = TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )


        self.item = self.model.objects.create(
            organization = self.organization,
            name = 'one-add'
        )

        self.other_org_item = self.model.objects.create(
            organization = self.different_organization,
            name = 'two-add'
        )


        self.url_view_kwargs = {'pk': self.item.id}

        self.add_data = {
            'name': 'team-post',
            'organization': self.organization.id,
        }


        self.add_data_import_fields = {
            'name': 'team-post',
            'organization': self.organization.id,
            'external_ref': 1,
            'external_system': int(Project.Ticket_ExternalSystem.CUSTOM_1)
        }


        self.add_user = User.objects.create_user(username="test_user_add", password="password")
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



class ProjectPermissionsAPI(ViewSetBase, APIPermissions, TestCase):


    def test_add_has_permission_no_import_fields(self):
        """ Check correct permission for add 

        Attempt to add as user with permission
        """

        client = Client()
        if self.url_kwargs:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')


        client.force_login(self.add_user)
        response = client.post(url, data=self.add_data_import_fields)

        assert (
            response.status_code == 201
            and response.data['external_ref'] is None
            and response.data['external_system'] is None
        )



    def test_add_has_permission_import_fields(self):
        """ Check correct permission for add 

        Attempt to add as user with permission
        """

        client = Client()
        if self.url_kwargs:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')


        client.force_login(self.import_user)
        response = client.post(url, data=self.add_data_import_fields)

        assert (
            response.status_code == 201
            and response.data['external_ref'] == 1
            and response.data['external_system'] == int(Project.Ticket_ExternalSystem.CUSTOM_1)
        )



class ProjectViewSet(ViewSetBase, SerializersTestCases, TestCase):

    pass



class ProjectMetadata(
    ViewSetBase,
    MetaDataNavigationEntriesFunctional,
    MetadataAttributesFunctional,
    TestCase
):

    menu_id = 'project_management'

    menu_entry_id = 'project'
