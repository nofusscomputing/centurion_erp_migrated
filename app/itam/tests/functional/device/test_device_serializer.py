import pytest

from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models import Organization

from itam.serializers.device import Device, DeviceModelSerializer



class DeviceValidationAPI(
    TestCase,
):

    model = Device

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        2. Create an item
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.item = self.model.objects.create(
            organization=organization,
            name = 'valid-hostname',
        )



    def test_serializer_validation_no_name(self):
        """Serializer Validation Check

        Ensure that if creating and no name is provided a validation error occurs
        """

        with pytest.raises(ValidationError) as err:

            serializer = DeviceModelSerializer(data={
                "organization": self.organization.id,
            })

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['name'][0] == 'required'



    def test_serializer_validation_update_existing_invalid_name_starts_with_digit(self):
        """Serializer Validation Check

        Ensure that if an existing item is given an invalid name 'starts with digit'
        it raises a validation error
        """

        with pytest.raises(ValidationError) as err:

            serializer = DeviceModelSerializer(
                self.item,
                data={
                    "name": '0-start-with-number'
                },
                partial=True,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['name'][0] == 'invalid_hostname'



    def test_serializer_validation_update_existing_invalid_name_contains_hyphon(self):
        """Serializer Validation Check

        Ensure that if an existing item is given an invalid name 'contains hyphon'
        it raises a validation error
        """

        with pytest.raises(ValidationError) as err:

            serializer = DeviceModelSerializer(
                self.item,
                data={
                    "name": 'has_a_hyphon'
                },
                partial=True,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['name'][0] == 'invalid_hostname'



    def test_serializer_validation_update_existing_invalid_name_ends_with_dash(self):
        """Serializer Validation Check

        Ensure that if an existing item is given an invalid name 'ends with dash'
        it raises a validation error
        """

        with pytest.raises(ValidationError) as err:

            serializer = DeviceModelSerializer(
                self.item,
                data={
                    "name": 'ends-with-dash-'
                },
                partial=True,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['name'][0] == 'invalid_hostname'



    def test_serializer_validation_update_existing_invalid_uuid_first_octet(self):
        """Serializer Validation Check

        Ensure that if an existing item is given an invalid uuid 'first octet not hex'
        it raises a validation error
        """

        with pytest.raises(ValidationError) as err:

            serializer = DeviceModelSerializer(
                self.item,
                data={
                    "uuid": 'g0000000-0000-0000-0000-000000000000'
                },
                partial=True,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['uuid'][0] == 'invalid_uuid'



    def test_serializer_validation_update_existing_invalid_uuid_first_octet_wrong_length(self):
        """Serializer Validation Check

        Ensure that if an existing item is given an invalid uuid 'first octet wrong length'
        it raises a validation error
        """

        with pytest.raises(ValidationError) as err:

            serializer = DeviceModelSerializer(
                self.item,
                data={
                    "uuid": '0000000-0000-0000-0000-000000000000'
                },
                partial=True,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['uuid'][0] == 'invalid_uuid'



    def test_serializer_validation_update_existing_invalid_uuid_second_octet(self):
        """Serializer Validation Check

        Ensure that if an existing item is given an invalid uuid 'second octet not hex'
        it raises a validation error
        """

        with pytest.raises(ValidationError) as err:

            serializer = DeviceModelSerializer(
                self.item,
                data={
                    "uuid": '00000000-g000-0000-0000-000000000000'
                },
                partial=True,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['uuid'][0] == 'invalid_uuid'


    def test_serializer_validation_update_existing_invalid_uuid_second_octet_wrong_length(self):
        """Serializer Validation Check

        Ensure that if an existing item is given an invalid uuid 'second octet wrong length'
        it raises a validation error
        """

        with pytest.raises(ValidationError) as err:

            serializer = DeviceModelSerializer(
                self.item,
                data={
                    "uuid": '00000000-000-0000-0000-000000000000'
                },
                partial=True,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['uuid'][0] == 'invalid_uuid'



    def test_serializer_validation_update_existing_invalid_uuid_third_octet(self):
        """Serializer Validation Check

        Ensure that if an existing item is given an invalid uuid 'third octet not hex'
        it raises a validation error
        """

        with pytest.raises(ValidationError) as err:

            serializer = DeviceModelSerializer(
                self.item,
                data={
                    "uuid": '00000000-0000-g000-0000-000000000000'
                },
                partial=True,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['uuid'][0] == 'invalid_uuid'


    def test_serializer_validation_update_existing_invalid_uuid_third_octet_wrong_length(self):
        """Serializer Validation Check

        Ensure that if an existing item is given an invalid uuid 'third octet wrong length'
        it raises a validation error
        """

        with pytest.raises(ValidationError) as err:

            serializer = DeviceModelSerializer(
                self.item,
                data={
                    "uuid": '00000000-0000-000-0000-000000000000'
                },
                partial=True,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['uuid'][0] == 'invalid_uuid'



    def test_serializer_validation_update_existing_invalid_uuid_fourth_octet(self):
        """Serializer Validation Check

        Ensure that if an existing item is given an invalid uuid 'fourth octet not hex'
        it raises a validation error
        """

        with pytest.raises(ValidationError) as err:

            serializer = DeviceModelSerializer(
                self.item,
                data={
                    "uuid": '00000000-0000-0000-g000-000000000000'
                },
                partial=True,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['uuid'][0] == 'invalid_uuid'


    def test_serializer_validation_update_existing_invalid_uuid_fourth_octet_wrong_length(self):
        """Serializer Validation Check

        Ensure that if an existing item is given an invalid uuid 'fourth octet wrong length'
        it raises a validation error
        """

        with pytest.raises(ValidationError) as err:

            serializer = DeviceModelSerializer(
                self.item,
                data={
                    "uuid": '00000000-0000-0000-000-000000000000'
                },
                partial=True,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['uuid'][0] == 'invalid_uuid'



    def test_serializer_validation_update_existing_invalid_uuid_fifth_octet(self):
        """Serializer Validation Check

        Ensure that if an existing item is given an invalid uuid 'fifth octet not hex'
        it raises a validation error
        """

        with pytest.raises(ValidationError) as err:

            serializer = DeviceModelSerializer(
                self.item,
                data={
                    "uuid": '00000000-0000-0000-0000-g00000000000'
                },
                partial=True,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['uuid'][0] == 'invalid_uuid'


    def test_serializer_validation_update_existing_invalid_uuid_fifth_octet_wrong_length(self):
        """Serializer Validation Check

        Ensure that if an existing item is given an invalid uuid 'fifth octet wrong length'
        it raises a validation error
        """

        with pytest.raises(ValidationError) as err:

            serializer = DeviceModelSerializer(
                self.item,
                data={
                    "uuid": '00000000-0000-0000-0000-00000000000'
                },
                partial=True,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['uuid'][0] == 'invalid_uuid'
