import pytest

from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.middleware.auth import Tenancy
from access.models import Organization

from itam.serializers.device_software import Device, DeviceSoftware, DeviceSoftwareModelSerializer, SoftwareInstallsModelSerializer
from itam.models.software import Software, SoftwareCategory, SoftwareVersion

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



class SoftwareInstallsValidationAPI(
    TestCase,
):

    model = DeviceSoftware

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        2. Create an item
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.user = User.objects.create(username = 'org_user', password='random password')

        self.software_category = SoftwareCategory.objects.create(
            organization=organization,
            name = 'category'
        )

        self.software = Software.objects.create(
            organization=organization,
            name = 'software',
            category = self.software_category
        )

        self.software_version = SoftwareVersion.objects.create(
            organization=organization,
            name = '12',
            software = self.software
        )

        self.device = Device.objects.create(
            organization=organization,
            name = 'device'
        )


        self.item = self.model.objects.create(
            organization=self.organization,
            software = self.software,
            version = self.software_version,
            device = self.device
        )

        self.valid_data: dict = {
            'organization': self.organization.pk,
            # 'software': self.software.pk,
            'version': self.software_version.pk,
            'device': self.device.pk
        }


    def test_serializer_validation_create(self):
        """Serializer Validation Check

        Ensure that an item can be created
        """


        mock_view = MockView( user = self.user )

        mock_view.kwargs = {
            'software_id': self.software.pk
        }

        data = self.valid_data.copy()


        serializer = SoftwareInstallsModelSerializer(
            context = {
                'request': mock_view.request,
                'view': mock_view
            },
            data = data
        )

        assert serializer.is_valid(raise_exception = True)



    def test_serializer_validation_no_device(self):
        """Serializer Validation Check

        Ensure that if creating and no device is provided a validation exception is thrown
        """

        mock_view = MockView( user = self.user )

        mock_view.kwargs = {
            'software_id': self.software.pk
        }

        data = self.valid_data.copy()

        del data['device']

        with pytest.raises(ValidationError) as err:

            serializer = SoftwareInstallsModelSerializer(
                context = {
                'request': mock_view.request,
                'view': mock_view
                },
                data = data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['device'][0] == 'required'



    def test_serializer_validation_no_software(self):
        """Serializer Validation Check

        Ensure that if creating and no software is provided no validation error
        occurs as the serializer provides the device from the view.
        """

        mock_view = MockView( user = self.user )

        mock_view.kwargs = {
            'software_id': self.software.pk
        }

        data = self.valid_data.copy()

        # del data['software']

        serializer = SoftwareInstallsModelSerializer(
            context = {
                'request': mock_view.request,
                'view': mock_view
            },
            data = data
        )

        assert serializer.is_valid(raise_exception = True)
