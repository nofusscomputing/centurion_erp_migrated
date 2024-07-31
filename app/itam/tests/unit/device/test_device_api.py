import pytest
import unittest

from django.contrib.auth.models import AnonymousUser, User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from rest_framework.relations import Hyperlink

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_permissions import APIPermissions

from config_management.models.groups import ConfigGroups, ConfigGroupHosts

from itam.models.device import Device


class DeviceAPI(TestCase):


    model = Device


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a device
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        different_organization = Organization.objects.create(name='test_different_organization')


        self.item = self.model.objects.create(
            organization=organization,
            name = 'deviceone',
            uuid = 'val',
            serial_number = 'another val'
        )

        config_group = ConfigGroups.objects.create(
            organization = self.organization,
            name = 'one',
            config = dict({"key": "one", "existing": "dont_over_write"})
        )

        config_group_second_item = ConfigGroups.objects.create(
            organization = self.organization,
            name = 'one_two',
            config = dict({"key": "two"}),
            parent = config_group
        )

        config_group_hosts = ConfigGroupHosts.objects.create(
            organization = organization,
            host = self.item,
            group = config_group,
        )


        config_group_hosts_two = ConfigGroupHosts.objects.create(
            organization = organization,
            host = self.item,
            group = config_group_second_item,
        )


        # self.url_kwargs = {'pk': self.item.id}

        self.url_view_kwargs = {'pk': self.item.id}

        # self.add_data = {'name': 'device', 'organization': self.organization.id}


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



        # add_permissions = Permission.objects.get(
        #         codename = 'add_' + self.model._meta.model_name,
        #         content_type = ContentType.objects.get(
        #             app_label = self.model._meta.app_label,
        #             model = self.model._meta.model_name,
        #         )
        #     )

        # add_team = Team.objects.create(
        #     team_name = 'add_team',
        #     organization = organization,
        # )

        # add_team.permissions.set([add_permissions])



        # change_permissions = Permission.objects.get(
        #         codename = 'change_' + self.model._meta.model_name,
        #         content_type = ContentType.objects.get(
        #             app_label = self.model._meta.app_label,
        #             model = self.model._meta.model_name,
        #         )
        #     )

        # change_team = Team.objects.create(
        #     team_name = 'change_team',
        #     organization = organization,
        # )

        # change_team.permissions.set([change_permissions])



        # delete_permissions = Permission.objects.get(
        #         codename = 'delete_' + self.model._meta.model_name,
        #         content_type = ContentType.objects.get(
        #             app_label = self.model._meta.app_label,
        #             model = self.model._meta.model_name,
        #         )
        #     )

        # delete_team = Team.objects.create(
        #     team_name = 'delete_team',
        #     organization = organization,
        # )

        # delete_team.permissions.set([delete_permissions])


        # self.no_permissions_user = User.objects.create_user(username="test_no_permissions", password="password")


        self.view_user = User.objects.create_user(username="test_user_view", password="password")
        teamuser = TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )

        # self.add_user = User.objects.create_user(username="test_user_add", password="password")
        # teamuser = TeamUsers.objects.create(
        #     team = add_team,
        #     user = self.add_user
        # )

        # self.change_user = User.objects.create_user(username="test_user_change", password="password")
        # teamuser = TeamUsers.objects.create(
        #     team = change_team,
        #     user = self.change_user
        # )

        # self.delete_user = User.objects.create_user(username="test_user_delete", password="password")
        # teamuser = TeamUsers.objects.create(
        #     team = delete_team,
        #     user = self.delete_user
        # )


        # self.different_organization_user = User.objects.create_user(username="test_different_organization_user", password="password")


        # different_organization_team = Team.objects.create(
        #     team_name = 'different_organization_team',
        #     organization = different_organization,
        # )

        # different_organization_team.permissions.set([
        #     view_permissions,
        #     add_permissions,
        #     change_permissions,
        #     delete_permissions,
        # ])

        # TeamUsers.objects.create(
        #     team = different_organization_team,
        #     user = self.different_organization_user
        # )


        client = Client()
        url = reverse('API:device-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data = response.data


    def test_api_field_exists_id(self):
        """ Test for existance of API Field

        id field must exist
        """

        assert 'id' in self.api_data


    def test_api_field_type_id(self):
        """ Test for type for API Field

        id field must be int
        """

        assert type(self.api_data['id']) is int


    def test_api_field_exists_is_global(self):
        """ Test for existance of API Field

        is_global field must exist
        """

        assert 'is_global' in self.api_data


    def test_api_field_type_is_global(self):
        """ Test for type for API Field

        is_global field must be boolean
        """

        assert type(self.api_data['is_global']) is bool


    def test_api_field_exists_name(self):
        """ Test for existance of API Field

        name field must exist
        """

        assert 'name' in self.api_data


    def test_api_field_type_name(self):
        """ Test for type for API Field

        name field must be str
        """

        assert type(self.api_data['name']) is str


    def test_api_field_exists_config(self):
        """ Test for existance of API Field

        config field must exist
        """

        assert 'config' in self.api_data


    def test_api_field_type_config(self):
        """ Test for type for API Field

        config field must be dict
        """

        assert type(self.api_data['config']) is str


    def test_api_field_exists_serial_number(self):
        """ Test for existance of API Field

        serial_number field must exist
        """

        assert 'serial_number' in self.api_data


    def test_api_field_type_serial_number(self):
        """ Test for type for API Field

        serial_number field must be str
        """

        assert type(self.api_data['serial_number']) is str


    def test_api_field_exists_uuid(self):
        """ Test for existance of API Field

        uuid field must exist
        """

        assert 'uuid' in self.api_data


    def test_api_field_type_uuid(self):
        """ Test for type for API Field

        uuid field must be str
        """

        assert type(self.api_data['uuid']) is str


    def test_api_field_exists_inventorydate(self):
        """ Test for existance of API Field

        inventorydate field must exist
        """

        assert 'inventorydate' in self.api_data


    def test_api_field_type_inventorydate(self):
        """ Test for type for API Field

        inventorydate field must be str
        """

        assert (
            type(self.api_data['inventorydate']) is str
            or
            self.api_data['inventorydate'] is None
        )


    def test_api_field_exists_created(self):
        """ Test for existance of API Field

        created field must exist
        """

        assert 'created' in self.api_data


    def test_api_field_type_created(self):
        """ Test for type for API Field

        created field must be str
        """

        assert type(self.api_data['created']) is str


    def test_api_field_exists_modified(self):
        """ Test for existance of API Field

        modified field must exist
        """

        assert 'modified' in self.api_data


    def test_api_field_type_modified(self):
        """ Test for type for API Field

        modified field must be str
        """

        assert type(self.api_data['modified']) is str


    def test_api_field_exists_groups(self):
        """ Test for existance of API Field

        groups field must exist
        """

        assert 'groups' in self.api_data


    def test_api_field_type_groups(self):
        """ Test for type for API Field

        groups field must be list
        """

        assert type(self.api_data['groups']) is list


    def test_api_field_exists_organization(self):
        """ Test for existance of API Field

        organization field must exist
        """

        assert 'organization' in self.api_data


    def test_api_field_type_organization(self):
        """ Test for type for API Field

        organization field must be dict
        """

        assert type(self.api_data['organization']) is dict


    def test_api_field_exists_url(self):
        """ Test for existance of API Field

        url field must exist
        """

        assert 'url' in self.api_data


    def test_api_field_type_url(self):
        """ Test for type for API Field

        url field must be str
        """

        assert type(self.api_data['url']) is Hyperlink




    def test_api_field_exists_organization_id(self):
        """ Test for existance of API Field

        organization.id field must exist
        """

        assert 'id' in self.api_data['organization']


    def test_api_field_type_organization_id(self):
        """ Test for type for API Field

        organization.id field must be int
        """

        assert type(self.api_data['organization']['id']) is int


    def test_api_field_exists_organization_name(self):
        """ Test for existance of API Field

        organization.name field must exist
        """

        assert 'name' in self.api_data['organization']


    def test_api_field_type_organization_name(self):
        """ Test for type for API Field

        organization.name field must be str
        """

        assert type(self.api_data['organization']['name']) is str




    def test_api_field_exists_groups_id(self):
        """ Test for existance of API Field

        groups.id field must exist
        """

        assert 'id' in self.api_data['groups'][0]


    def test_api_field_type_groups_id(self):
        """ Test for type for API Field

        groups.id field must be int
        """

        assert type(self.api_data['groups'][0]['id']) is int


    def test_api_field_exists_groups_name(self):
        """ Test for existance of API Field

        groups.name field must exist
        """

        assert 'name' in self.api_data['groups'][0]


    def test_api_field_type_groups_name(self):
        """ Test for type for API Field

        groups.name field must be str
        """

        assert type(self.api_data['groups'][0]['name']) is str


    def test_api_field_exists_groups_url(self):
        """ Test for existance of API Field

        groups.url field must exist
        """

        assert 'url' in self.api_data['groups'][0]


    def test_api_field_type_groups_url(self):
        """ Test for type for API Field

        groups.url field must be str
        """

        assert type(self.api_data['groups'][0]['url']) is Hyperlink
