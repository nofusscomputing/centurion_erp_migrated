import pytest

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase
from django import urls

from django_celery_results.models import TaskResult

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_permissions_viewset import (
    APIPermissionAdd,
    APIPermissionChange,
    APIPermissionDelete,
    APIPermissionView
)

from settings.models.user_settings import UserSettings


class TaskResultPermissionsAPI(
    TestCase,
    APIPermissionAdd,
    APIPermissionChange,
    APIPermissionDelete,
    APIPermissionView
):
    """These tests are custom tests of test of the same name.
    
    This model is View Only for any authenticated user.
    """

    model = TaskResult

    app_namespace = 'v2'
    
    url_name = '_api_v2_celery_log'

    change_data = {'device_model_is_global': True}

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


        self.no_permissions_user = User.objects.create_user(username="test_no_permissions", password="password")


        self.view_user = User.objects.create_user(username="test_user_view", password="password")
        teamuser = TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )

        # self.item = self.model.objects.get( id = 1 )

        # self.item.default_organization = self.organization

        # self.item.save()


        self.item = self.model.objects.create(
            task_id = 'd15233ee-a14d-4135-afe5-e406b1b61330',
            task_name = 'itam.tasks.process_inventory',
            task_args = '{"random": "value"}',
            task_kwargs = 'sdas',
            status = "SUCCESS",
            worker = "debug-itsm@laptop2",
            content_type = "application/json",
            content_encoding = "utf-8",
            result = "finished...",
            traceback = "a trace",
            meta = 'meta',
            periodic_task_name = 'a name',
        )


        self.url_view_kwargs = {'pk': self.item.id}

        self.add_data = {
            'name': 'team-post',
            'organization': self.organization.id,
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


    def test_add_no_permission_denied(self):
        """ Check correct permission for add

        Attempt to add as user with no permissions
        """

        client = Client()
        if self.url_kwargs:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')


        client.force_login(self.no_permissions_user)
        response = client.post(url, data=self.add_data)

        assert response.status_code == 405


    # @pytest.mark.skip(reason="ToDO: figure out why fails")
    def test_add_different_organization_denied(self):
        """ Check correct permission for add

        attempt to add as user from different organization
        """

        client = Client()
        if self.url_kwargs:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')


        client.force_login(self.different_organization_user)
        response = client.post(url, data=self.add_data)

        assert response.status_code == 405


    def test_add_permission_view_denied(self):
        """ Check correct permission for add

        Attempt to add a user with view permission
        """

        client = Client()
        if self.url_kwargs:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')


        client.force_login(self.view_user)
        response = client.post(url, data=self.add_data)

        assert response.status_code == 405




    def test_add_has_permission(self):
        """ Check correct permission for add 

        Attempt to add as user with permission
        """

        client = Client()
        if self.url_kwargs:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')


        client.force_login(self.add_user)
        response = client.post(url, data=self.add_data)

        assert response.status_code == 405






    def test_change_no_permission_denied(self):
        """ Ensure permission view cant make change

        Attempt to make change as user without permissions
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.no_permissions_user)
        response = client.patch(url, data=self.change_data, content_type='application/json')

        assert response.status_code == 405


    def test_change_different_organization_denied(self):
        """ Ensure permission view cant make change

        Attempt to make change as user from different organization
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.different_organization_user)
        response = client.patch(url, data=self.change_data, content_type='application/json')

        assert response.status_code == 405


    def test_change_permission_view_denied(self):
        """ Ensure permission view cant make change

        Attempt to make change as user with view permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.patch(url, data=self.change_data, content_type='application/json')

        assert response.status_code == 405


    def test_change_permission_add_denied(self):
        """ Ensure permission view cant make change

        Attempt to make change as user with add permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.add_user)
        response = client.patch(url, data=self.change_data, content_type='application/json')

        assert response.status_code == 405



    def test_change_has_permission(self):
        """ Check correct permission for change

        Make change with user who has change permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.change_user)
        response = client.patch(url, data=self.change_data, content_type='application/json')

        assert response.status_code == 405




    def test_delete_no_permission_denied(self):
        """ Check correct permission for delete

        Attempt to delete as user with no permissons
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.no_permissions_user)
        response = client.delete(url, data=self.delete_data)

        assert response.status_code == 405


    def test_delete_different_organization_denied(self):
        """ Check correct permission for delete

        Attempt to delete as user from different organization
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.different_organization_user)
        response = client.delete(url, data=self.delete_data)

        assert response.status_code == 405




    def test_delete_permission_view_denied(self):
        """ Check correct permission for delete

        Attempt to delete as user with veiw permission only
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.delete(url, data=self.delete_data)

        assert response.status_code == 405


    def test_delete_permission_add_denied(self):
        """ Check correct permission for delete

        Attempt to delete as user with add permission only
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.add_user)
        response = client.delete(url, data=self.delete_data)

        assert response.status_code == 405


    def test_delete_permission_change_denied(self):
        """ Check correct permission for delete

        Attempt to delete as user with change permission only
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.change_user)
        response = client.delete(url, data=self.delete_data)

        assert response.status_code == 405







    def test_delete_has_permission(self):
        """ Check correct permission for delete

        Delete item as user with delete permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.delete_user)
        response = client.delete(url, data=self.delete_data)

        assert response.status_code == 405


    def test_view_no_permission_denied(self):
        """ Check correct permission for view

        Attempt to view with user missing permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.no_permissions_user)
        response = client.get(url)

        assert response.status_code == 200


    def test_view_different_organizaiton_denied(self):
        """ Check correct permission for view

        Attempt to view with user from different organization
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.different_organization_user)
        response = client.get(url)

        assert response.status_code == 200


    def test_returned_results_only_user_orgs(self):
        """Test not required

        this test is not required as a task result
        is not a tenancy object that a user has any CRUD
        op to.
        """

        pass
