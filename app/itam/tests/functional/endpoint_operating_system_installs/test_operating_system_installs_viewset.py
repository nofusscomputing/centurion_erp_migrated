import pytest

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_permissions_viewset import APIPermissionView
from api.tests.abstract.api_serializer_viewset import SerializerView

from itam.serializers.device_operating_system import Device, DeviceOperatingSystem, DeviceOperatingSystemModelSerializer
from itam.models.operating_system import OperatingSystem, OperatingSystemVersion



class ViewSetBase:

    model = DeviceOperatingSystem

    app_namespace = 'v2'
    
    url_name = '_api_v2_operating_system_installs'

    change_data = {'name': '1.1'}

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


        change_permissions = Permission.objects.get(
                codename = 'change_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )


        delete_permissions = Permission.objects.get(
                codename = 'delete_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        self.no_permissions_user = User.objects.create_user(username="test_no_permissions", password="password")


        self.view_user = User.objects.create_user(username="test_user_view", password="password")
        teamuser = TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )


        self.operating_system = OperatingSystem.objects.create(
            organization=organization,
            name = '12',
        )

        self.operating_system_version = OperatingSystemVersion.objects.create(
            organization=organization,
            name = '12',
            operating_system = self.operating_system
        )

        self.device = Device.objects.create(
            organization=organization,
            name = 'device'
        )


        self.item = self.model.objects.create(
            organization=self.organization,
            version = '1',
            operating_system_version = self.operating_system_version,
            device = self.device
        )


        self.url_view_kwargs = {'operating_system_id': self.operating_system_version.operating_system.pk, 'pk': self.item.id}


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



class OperatingSystemInstallsPermissionsAPI(
    ViewSetBase,
    APIPermissionView,
    TestCase
):

    pass



class OperatingSystemInstallsViewSet(
    ViewSetBase,
    SerializerView,
    TestCase
):

    pass
