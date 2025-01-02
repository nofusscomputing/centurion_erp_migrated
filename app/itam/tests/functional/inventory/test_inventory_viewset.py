import copy
import pytest

from unittest.mock import patch

from django.contrib.auth.models import AnonymousUser, User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_serializer_viewset import SerializersTestCases
from api.tests.abstract.api_permissions_viewset import (
    APIPermissionAdd,
    APIPermissionChange
)
from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional, MetaDataNavigationEntriesFunctional

from itam.models.device import Device
from itam.tasks.inventory import process_inventory

from settings.models.user_settings import UserSettings



class ViewSetBase:

    model = Device

    app_namespace = 'v2'
    
    url_name = '_api_v2_inventory'

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


        self.item = self.model.objects.create(
            organization = self.organization,
            name = 'one-add'
        )

        self.other_org_item = self.model.objects.create(
            organization = different_organization,
            name = 'other_item'
        )


        self.add_user = User.objects.create_user(username="test_user_add", password="password")
        teamuser = TeamUsers.objects.create(
            team = add_team,
            user = self.add_user
        )

        user_settings = UserSettings.objects.get(
            user = self.add_user
        )
        user_settings.default_organization = self.organization
        user_settings.save()




        self.change_user = User.objects.create_user(username="test_user_change", password="password")
        teamuser = TeamUsers.objects.create(
            team = change_team,
            user = self.change_user
        )

        user_settings = UserSettings.objects.get(
            user = self.change_user
        )
        user_settings.default_organization = self.organization
        user_settings.save()



        self.delete_user = User.objects.create_user(username="test_user_delete", password="password")
        teamuser = TeamUsers.objects.create(
            team = delete_team,
            user = self.delete_user
        )


        self.different_organization_user = User.objects.create_user(username="test_different_organization_user", password="password")

        user_settings = UserSettings.objects.get(
            user = self.different_organization_user
        )
        user_settings.default_organization = different_organization
        user_settings.save()


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


        self.inventory: dict = {
            "details": {
                "name": "string",
                "serial_number": "string",
                "uuid": "fc65b513-3ddc-4c90-af20-215b2db73455"
            },
            "os": {
                "name": "string",
                "version_major": 1,
                "version": "1.2"
            },
            "software": [
                {
                "name": "string",
                "category": "string",
                "version": "1.1.1"
                }
            ]
        }

        self.add_data = copy.deepcopy(self.inventory)

        self.change_data = copy.deepcopy(self.inventory)

        self.change_data['details']['name'] = 'device2'
        self.change_data['details']['serial_number'] = 'sn123'
        self.change_data['details']['uuid'] = '93e8e991-ad07-4b7b-a1a6-59968a5b54f8'

        Device.objects.create(
            organization = self.organization,
            name = self.change_data['details']['name'],
            serial_number = self.change_data['details']['serial_number'],
            uuid = self.change_data['details']['uuid'],
        )



class DevicePermissionsAPI(
    ViewSetBase,
    # APIPermissionAdd,
    # APIPermissionChange,
    TestCase
):

    url_kwargs = None

    url_view_kwargs = None


    @patch.object(process_inventory, 'delay')
    def test_add_has_permission(self, process_inventory):
        """ Check correct permission for add

        This test case is a over-ride of a test case with the same name.
        This was done as the testcase needed to be modified to work with the
        itam inventory endpoint.

        Attempt to add as user with permission
        """

        client = Client()
        if self.url_kwargs:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')


        client.force_login(self.add_user)
        response = client.post(url, data=self.add_data, content_type = 'application/json')

        assert response.status_code == 200






    @patch.object(process_inventory, 'delay')
    def test_add_user_anon_denied(self, process_inventory):
        """ Check correct permission for add 

        Attempt to add as anon user
        """

        client = Client()
        if self.url_kwargs:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')


        response = client.put(url, data=self.add_data)

        assert response.status_code == 401


    @patch.object(process_inventory, 'delay')
    def test_add_no_permission_denied(self, process_inventory):
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

        assert response.status_code == 403


    # # @pytest.mark.skip(reason="ToDO: figure out why fails")
    # def test_add_different_organization_denied(self):
    #     """ Check correct permission for add

    #     attempt to add as user from different organization
    #     """

    #     client = Client()
    #     if self.url_kwargs:

    #         url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

    #     else:

    #         url = reverse(self.app_namespace + ':' + self.url_name + '-list')


    #     client.force_login(self.different_organization_user)
    #     response = client.post(url, data=self.add_data)

    #     assert response.status_code == 403


    @patch.object(process_inventory, 'delay')
    def test_add_permission_view_denied(self, process_inventory):
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

        assert response.status_code == 403


















    @patch.object(process_inventory, 'delay')
    def test_change_has_permission(self, process_inventory):
        """ Check correct permission for change

        This test case is a over-ride of a test case with the same name.
        This was done as the testcase needed to be modified to work with the
        itam inventory endpoint.

        Make change with user who has change permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs=self.url_view_kwargs)


        client.force_login(self.change_user)
        response = client.post(url, data=self.change_data, content_type='application/json')

        assert response.status_code == 200















    @patch.object(process_inventory, 'delay')
    def test_change_user_anon_denied(self, process_inventory):
        """ Check correct permission for change

        Attempt to change as anon
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs=self.url_view_kwargs)


        response = client.post(url, data=self.change_data, content_type='application/json')

        assert response.status_code == 401


    @patch.object(process_inventory, 'delay')
    def test_change_no_permission_denied(self, process_inventory):
        """ Ensure permission view cant make change

        Attempt to make change as user without permissions
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs=self.url_view_kwargs)


        client.force_login(self.no_permissions_user)
        response = client.post(url, data=self.change_data, content_type='application/json')

        assert response.status_code == 403



    @patch.object(process_inventory, 'delay')
    def test_change_different_organization_denied(self, process_inventory):
        """ Ensure permission view cant make change

        Attempt to make change as user from different organization
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs=self.url_view_kwargs)


        client.force_login(self.different_organization_user)
        response = client.post(url, data=self.change_data, content_type='application/json')

        assert response.status_code == 403



    @patch.object(process_inventory, 'delay')
    def test_change_permission_view_denied(self, process_inventory):
        """ Ensure permission view cant make change

        Attempt to make change as user with view permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.post(url, data=self.change_data, content_type='application/json')

        assert response.status_code == 403


    @patch.object(process_inventory, 'delay')
    def test_change_permission_add_denied(self, process_inventory):
        """ Ensure permission view cant make change

        Attempt to make change as user with add permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs=self.url_view_kwargs)


        client.force_login(self.add_user)
        response = client.post(url, data=self.change_data, content_type='application/json')

        assert response.status_code == 403




# class DeviceViewSet(
#     ViewSetBase,
#     SerializersTestCases,
#     TestCase
# ):

#     pass



# class DeviceMetadata(
#     ViewSetBase,
#     MetadataAttributesFunctional,
#     MetaDataNavigationEntriesFunctional,
#     TestCase
# ):

#     menu_id = 'itam'

#     menu_entry_id = 'device'
