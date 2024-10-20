import pytest

from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models import Organization

from itam.serializers.device_software import Device, DeviceSoftware, DeviceSoftwareModelSerializer
from itam.models.software import Software, SoftwareCategory, SoftwareVersion



class DeviceSoftwareValidationAPI(
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



    def test_serializer_validation_create(self):
        """Serializer Validation Check

        Ensure that an item can be created
        """

        serializer = DeviceSoftwareModelSerializer(data={
            'organization': self.organization.pk,
            'software': self.software.pk,
            'version': self.software_version.pk,
            'device': self.device.pk
        })

        assert serializer.is_valid(raise_exception = True)


    def test_serializer_validation_no_device(self):
        """Serializer Validation Check

        Ensure that if creating and no device is provided a validation exception is thrown
        """

        with pytest.raises(ValidationError) as err:

            serializer = DeviceSoftwareModelSerializer(data={
                'organization': self.organization.pk,
                'software': self.software.pk,
                'version': self.software_version.pk,
            })

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['device'][0] == 'required'


    def test_serializer_validation_no_software(self):
        """Serializer Validation Check

        Ensure that if creating and no device is provided a validation exception is thrown
        """

        with pytest.raises(ValidationError) as err:

            serializer = DeviceSoftwareModelSerializer(data={
                'organization': self.organization.pk,
                'version': self.software_version.pk,
                'device': self.device.pk
            })

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['software'][0] == 'required'
