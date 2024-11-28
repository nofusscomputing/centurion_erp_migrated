import pytest

from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models import Organization

from itim.serializers.port import Port, PortModelSerializer



class PortValidationAPI(
    TestCase,
):

    model = Port

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        # 2. Create an item
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        # self.item = self.model.objects.create(
        #     organization=organization,
        #     number = 'os name',
        # )



    def test_serializer_validation_can_create(self):
        """Serializer Validation Check

        Ensure that a valid item has no validation errors
        """

        serializer = PortModelSerializer(data={
            "organization": self.organization.id,
            "number": 80,
            "protocol": Port.Protocol.TCP
        })

        assert serializer.is_valid(raise_exception = True)



    def test_serializer_validation_no_number(self):
        """Serializer Validation Check

        Ensure that if creating and no number is provided a validation error occurs
        """

        with pytest.raises(ValidationError) as err:

            serializer = PortModelSerializer(data={
                "organization": self.organization.id,
                # "number": 80,
                "protocol": Port.Protocol.TCP
            })

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['number'][0] == 'required'



    def test_serializer_validation_no_protocol(self):
        """Serializer Validation Check

        Ensure that if creating and no protocol is provided a validation error occurs
        """

        with pytest.raises(ValidationError) as err:

            serializer = PortModelSerializer(data={
                "organization": self.organization.id,
                "number": 80,
                # "protocol": Port.Protocol.TCP
            })

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['protocol'][0] == 'required'
