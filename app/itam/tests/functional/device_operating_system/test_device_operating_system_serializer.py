import pytest

from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.middleware.request import Tenancy
from access.models import Organization

from itam.serializers.device_operating_system import Device, DeviceOperatingSystem, DeviceOperatingSystemModelSerializer
from itam.models.operating_system import OperatingSystem, OperatingSystemVersion

from settings.models.app_settings import AppSettings



class MockView:

    action: str = None

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



class DeviceOperatingSystemValidationAPI(
    TestCase,
):

    model = DeviceOperatingSystem

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        2. Create an item
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.user = User.objects.create(username = 'org_user', password='random password')

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

        self.device_two = Device.objects.create(
            organization=organization,
            name = 'device-two'
        )


        self.item = self.model.objects.create(
            organization=self.organization,
            version = '1',
            operating_system_version = self.operating_system_version,
            device = self.device
        )

        self.valid_data = {
            'organization': self.organization.pk,
            'version': '1',
            'operating_system_version': self.operating_system_version.pk,
            'device': self.device_two.pk,
        }



    def test_serializer_validation_create(self):
        """Serializer Validation Check

        Ensure that an item can be created
        """

        mock_view = MockView( user = self.user )

        mock_view.kwargs = {
            'device_id': self.valid_data['device']
        }

        serializer = DeviceOperatingSystemModelSerializer(
            context = {
                'request': mock_view.request,
                'view': mock_view
            },
            data = self.valid_data
        )

        assert serializer.is_valid(raise_exception = True)


    def test_serializer_validation_no_device_success(self):
        """Serializer Validation Check

        Ensure that if creating and no device is provided no validation exception is thrown
        as the serializer supplies the device from the view kwargs
        """

        data = self.valid_data.copy()

        del data['device']

        mock_view = MockView( user = self.user )

        mock_view.kwargs = {
            'device_id': self.valid_data['device']
        }

        serializer = DeviceOperatingSystemModelSerializer(
            context = {
                'request': mock_view.request,
                'view': mock_view
            },
            data = data
        )

        assert serializer.is_valid(raise_exception = True)


    def test_serializer_validation_no_operating_system_version(self):
        """Serializer Validation Check

        Ensure that if creating and no operating_system_version is provided a validation exception is thrown
        """

        data = self.valid_data.copy()

        del data['operating_system_version']

        mock_view = MockView( user = self.user )

        mock_view.kwargs = {
            'device_id': self.valid_data['device']
        }

        with pytest.raises(ValidationError) as err:

            serializer = DeviceOperatingSystemModelSerializer(
                context = {
                    'request': mock_view.request,
                    'view': mock_view
                },
                data = data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['operating_system_version'][0] == 'required'
