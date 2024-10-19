import pytest

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from rest_framework.relations import Hyperlink

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_fields import APITenancyObject

from core.models.notes import Notes

from itam.models.device import Device
from itam.models.operating_system import OperatingSystem
from itam.models.software import Software



class NotesAPI(
    TestCase,
    APITenancyObject
):

    model = Notes

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create an item

        """

        self.organization = Organization.objects.create(name='test_org')

        self.device = Device.objects.create(
            organization = self.organization,
            name = 'notes-device'
        )

        self.operating_system = OperatingSystem.objects.create(
            organization = self.organization,
            name = 'notes-os'
        )

        self.software = Software.objects.create(
            organization = self.organization,
            name = 'notes-software'
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


        self.item = self.model.objects.create(
            organization = self.organization,
            note = 'one',
            device = self.device,
            operatingsystem = self.operating_system,
            software = self.software,
            usercreated = self.view_user,
            usermodified = self.view_user
        )

        self.second_item = self.model.objects.create(
            organization = self.organization,
            note = 'one_two',
            device = self.device
        )

        self.url_view_kwargs = {'device_id': self.device.id, 'pk': self.item.id}


        client = Client()
        url = reverse('API:_api_v2_device_notes-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data = response.data




    def test_api_field_exists_model_notes(self):
        """ Test for existance of API Field

        This test is a custome test case from a test with the same name. It
        exists as this model does not have a model_notes field.

        model_notes field must exist
        """

        assert 'model_notes' not in self.api_data


    def test_api_field_type_model_notes(self):
        """ Test for type for API Field

        This test is a custome test case from a test with the same name. It
        exists as this model does not have a model_notes field.

        model_notes field must be str
        """

        pass



    def test_api_field_exists_note(self):
        """ Test for existance of API Field

        model_nonotetes field must exist
        """

        assert 'note' in self.api_data


    def test_api_field_type_note(self):
        """ Test for type for API Field

        note field must be str
        """

        assert type(self.api_data['note']) is str



    def test_api_field_exists_usercreated(self):
        """ Test for existance of API Field

        usercreated field must exist
        """

        assert 'usercreated' in self.api_data


    def test_api_field_type_usercreated(self):
        """ Test for type for API Field

        usercreated field must be dict
        """

        assert type(self.api_data['usercreated']) is dict


    def test_api_field_exists_usercreated_id(self):
        """ Test for existance of API Field

        usercreated.id field must exist
        """

        assert 'id' in self.api_data['usercreated']


    def test_api_field_type_usercreated_id(self):
        """ Test for type for API Field

        usercreated.id field must be int
        """

        assert type(self.api_data['usercreated']['id']) is int


    def test_api_field_exists_usercreated_display_name(self):
        """ Test for existance of API Field

        usercreated.display_name field must exist
        """

        assert 'display_name' in self.api_data['usercreated']


    def test_api_field_type_usercreated_display_name(self):
        """ Test for type for API Field

        usercreated.display_name field must be str
        """

        assert type(self.api_data['usercreated']['display_name']) is str


    def test_api_field_exists_usercreated_url(self):
        """ Test for existance of API Field

        usercreated.url field must exist
        """

        assert 'url' in self.api_data['usercreated']


    def test_api_field_type_usercreated_url(self):
        """ Test for type for API Field

        usercreated.url field must be Hyperlink
        """

        assert type(self.api_data['usercreated']['url']) is Hyperlink



    def test_api_field_exists_usermodified(self):
        """ Test for existance of API Field

        usermodified field must exist
        """

        assert 'usermodified' in self.api_data


    def test_api_field_type_usermodified(self):
        """ Test for type for API Field

        usermodified field must be dict
        """

        assert type(self.api_data['usermodified']) is dict


    def test_api_field_exists_usermodified_id(self):
        """ Test for existance of API Field

        usermodified.id field must exist
        """

        assert 'id' in self.api_data['usermodified']


    def test_api_field_type_usermodified_id(self):
        """ Test for type for API Field

        usermodified.id field must be int
        """

        assert type(self.api_data['usermodified']['id']) is int


    def test_api_field_exists_usermodified_display_name(self):
        """ Test for existance of API Field

        usermodified.display_name field must exist
        """

        assert 'display_name' in self.api_data['usermodified']


    def test_api_field_type_usermodified_display_name(self):
        """ Test for type for API Field

        usermodified.display_name field must be str
        """

        assert type(self.api_data['usermodified']['display_name']) is str


    def test_api_field_exists_usermodified_url(self):
        """ Test for existance of API Field

        usermodified.url field must exist
        """

        assert 'url' in self.api_data['usermodified']


    def test_api_field_type_usermodified_url(self):
        """ Test for type for API Field

        usermodified.url field must be Hyperlink
        """

        assert type(self.api_data['usermodified']['url']) is Hyperlink



    def test_api_field_exists_device(self):
        """ Test for existance of API Field

        device field must exist
        """

        assert 'device' in self.api_data


    def test_api_field_type_device(self):
        """ Test for type for API Field

        device field must be dict
        """

        assert type(self.api_data['device']) is dict


    def test_api_field_exists_device_id(self):
        """ Test for existance of API Field

        device.id field must exist
        """

        assert 'id' in self.api_data['device']


    def test_api_field_type_device_id(self):
        """ Test for type for API Field

        device.id field must be int
        """

        assert type(self.api_data['device']['id']) is int


    def test_api_field_exists_device_display_name(self):
        """ Test for existance of API Field

        device.display_name field must exist
        """

        assert 'display_name' in self.api_data['device']


    def test_api_field_type_device_display_name(self):
        """ Test for type for API Field

        device.display_name field must be str
        """

        assert type(self.api_data['device']['display_name']) is str


    def test_api_field_exists_device_url(self):
        """ Test for existance of API Field

        device.url field must exist
        """

        assert 'url' in self.api_data['device']


    def test_api_field_type_device_url(self):
        """ Test for type for API Field

        device.url field must be str
        """

        assert type(self.api_data['device']['url']) is str



    def test_api_field_exists_operatingsystem(self):
        """ Test for existance of API Field

        operatingsystemfield must exist
        """

        assert 'operatingsystem' in self.api_data


    def test_api_field_type_operatingsystem(self):
        """ Test for type for API Field

        operatingsystemfield must be dict
        """

        assert type(self.api_data['operatingsystem']) is dict


    def test_api_field_exists_operatingsystem_id(self):
        """ Test for existance of API Field

        operatingsystem.id field must exist
        """

        assert 'id' in self.api_data['operatingsystem']


    def test_api_field_type_operatingsystem_id(self):
        """ Test for type for API Field

        operatingsystem.id field must be int
        """

        assert type(self.api_data['operatingsystem']['id']) is int


    def test_api_field_exists_operatingsystem_display_name(self):
        """ Test for existance of API Field

        operatingsystem.display_name field must exist
        """

        assert 'display_name' in self.api_data['operatingsystem']


    def test_api_field_type_operatingsystem_display_name(self):
        """ Test for type for API Field

        operatingsystem.display_name field must be str
        """

        assert type(self.api_data['operatingsystem']['display_name']) is str


    def test_api_field_exists_operatingsystem_url(self):
        """ Test for existance of API Field

        operatingsystem.url field must exist
        """

        assert 'url' in self.api_data['operatingsystem']


    def test_api_field_type_operatingsystem_url(self):
        """ Test for type for API Field

        operatingsystem.url field must be Hyperlink
        """

        assert type(self.api_data['operatingsystem']['url']) is Hyperlink





    def test_api_field_exists_software(self):
        """ Test for existance of API Field

        software field must exist
        """

        assert 'software' in self.api_data


    def test_api_field_type_software(self):
        """ Test for type for API Field

        softwarefield must be dict
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

        software.url field must be Hyperlink
        """

        assert type(self.api_data['software']['url']) is Hyperlink

