import pytest
# import unittest

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from rest_framework.relations import Hyperlink

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_fields import APITenancyObject

from config_management.models.groups import DeviceSoftware, ConfigGroups, ConfigGroupSoftware, Software, SoftwareVersion



class ConfigGroupsAPI(
    TestCase,
    APITenancyObject
):

    model = ConfigGroupSoftware

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create an item

        """

        self.organization = Organization.objects.create(name='test_org')


        self.config_group = ConfigGroups.objects.create(
            organization = self.organization,
            name = 'one',
            config = dict({"key": "one", "existing": "dont_over_write"})
        )

        self.software = Software.objects.create(
            organization = self.organization,
            name = 'conf grp soft'
        )

        self.software_version = SoftwareVersion.objects.create(
            organization = self.organization,
            name = '1.1.1',
            software = self.software

        )

        self.item = self.model.objects.create(
            organization = self.organization,
            config_group = self.config_group,
            action = DeviceSoftware.Actions.INSTALL,
            software = self.software,
            version = self.software_version
        )

        self.url_view_kwargs = {'group_id': self.config_group.id, 'pk': self.item.id}

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

        client = Client()
        url = reverse('API:_api_v2_config_group_software-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data = response.data



    def test_api_field_exists_action(self):
        """ Test for existance of API Field

        action field must exist
        """

        assert 'action' in self.api_data


    def test_api_field_type_action(self):
        """ Test for type for API Field

        action field must be int
        """

        assert type(self.api_data['action']) is int



    def test_api_field_exists_model_notes(self):
        """ Test for existance of API Field

        model_notes field must not exist
        """

        assert 'model_notes' not in self.api_data


    def test_api_field_type_model_notes(self):
        """ Test for type for API Field

        model_notes does not exist for this model
        """

        assert True


    def test_api_field_exists_config_group(self):
        """ Test for existance of API Field

        config_group field must exist
        """

        assert 'config_group' in self.api_data


    def test_api_field_type_config_group(self):
        """ Test for type for API Field

        config_group field must be dict
        """

        assert type(self.api_data['config_group']) is dict



    def test_api_field_exists_config_group_id(self):
        """ Test for existance of API Field

        config_group.id field must exist
        """

        assert 'id' in self.api_data['config_group']


    def test_api_field_type_config_group_id(self):
        """ Test for type for API Field

        config_group.id field must be int
        """

        assert type(self.api_data['config_group']['id']) is int


    def test_api_field_exists_config_group_display_name(self):
        """ Test for existance of API Field

        config_group.display_name field must exist
        """

        assert 'display_name' in self.api_data['config_group']


    def test_api_field_type_config_group_display_name(self):
        """ Test for type for API Field

        config_group.display_name field must be str
        """

        assert type(self.api_data['config_group']['display_name']) is str


    def test_api_field_exists_config_group_url(self):
        """ Test for existance of API Field

        config_group.url field must exist
        """

        assert 'url' in self.api_data['config_group']


    def test_api_field_type_config_group_url(self):
        """ Test for type for API Field

        config_group.url field must be str
        """

        assert type(self.api_data['config_group']['url']) is str







    def test_api_field_exists_software(self):
        """ Test for existance of API Field

        software field must exist
        """

        assert 'software' in self.api_data


    def test_api_field_type_software(self):
        """ Test for type for API Field

        software field must be dict
        """

        assert type(self.api_data['software']) is dict



    def test_api_field_exists_software_id(self):
        """ Test for existance of API Field

        software.id field must exist
        """

        assert 'id' in self.api_data['software']


    def test_api_field_type_software_id(self):
        """ Test for type for API Field

        software.id field must be int
        """

        assert type(self.api_data['software']['id']) is int


    def test_api_field_exists_software_display_name(self):
        """ Test for existance of API Field

        software.display_name field must exist
        """

        assert 'display_name' in self.api_data['software']


    def test_api_field_type_software_display_name(self):
        """ Test for type for API Field

        software.display_name field must be str
        """

        assert type(self.api_data['software']['display_name']) is str


    def test_api_field_exists_software_url(self):
        """ Test for existance of API Field

        software.url field must exist
        """

        assert 'url' in self.api_data['software']


    def test_api_field_type_software_url(self):
        """ Test for type for API Field

        software.url field must be str
        """

        assert type(self.api_data['software']['url']) is Hyperlink








    def test_api_field_exists_version(self):
        """ Test for existance of API Field

        version field must exist
        """

        assert 'version' in self.api_data


    def test_api_field_type_version(self):
        """ Test for type for API Field

        version field must be dict
        """

        assert type(self.api_data['version']) is dict



    def test_api_field_exists_version_id(self):
        """ Test for existance of API Field

        version.id field must exist
        """

        assert 'id' in self.api_data['version']


    def test_api_field_type_version_id(self):
        """ Test for type for API Field

        version.id field must be int
        """

        assert type(self.api_data['version']['id']) is int


    def test_api_field_exists_version_display_name(self):
        """ Test for existance of API Field

        version.display_name field must exist
        """

        assert 'display_name' in self.api_data['version']


    def test_api_field_type_version_display_name(self):
        """ Test for type for API Field

        version.display_name field must be str
        """

        assert type(self.api_data['version']['display_name']) is str


    def test_api_field_exists_version_url(self):
        """ Test for existance of API Field

        version.url field must exist
        """

        assert 'url' in self.api_data['version']


    def test_api_field_type_version_url(self):
        """ Test for type for API Field

        version.url field must be Hyperlink
        """

        assert type(self.api_data['version']['url']) is Hyperlink
