import pytest

from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models import Organization

from itam.serializers.device_operating_system import Device, DeviceOperatingSystem, DeviceOperatingSystemModelSerializer
from itam.models.operating_system import OperatingSystem, OperatingSystemVersion



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

        serializer = DeviceOperatingSystemModelSerializer(
            data = self.valid_data
        )

        assert serializer.is_valid(raise_exception = True)


    def test_serializer_validation_no_device(self):
        """Serializer Validation Check

        Ensure that if creating and no device is provided a validation exception is thrown
        """

        data = self.valid_data.copy()

        del data['device']

        with pytest.raises(ValidationError) as err:

            serializer = DeviceOperatingSystemModelSerializer(
                data = data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['device'][0] == 'required'


    def test_serializer_validation_no_operating_system_version(self):
        """Serializer Validation Check

        Ensure that if creating and no operating_system_version is provided a validation exception is thrown
        """

        data = self.valid_data.copy()

        del data['operating_system_version']

        with pytest.raises(ValidationError) as err:

            serializer = DeviceOperatingSystemModelSerializer(
                data = data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['operating_system_version'][0] == 'required'
