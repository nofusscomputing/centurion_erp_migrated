import pytest

from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models import Organization

from itam.serializers.inventory import (
    InventorySerializer
)



class InventoryValidationAPI(
    TestCase,
):


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        2. Create an item
        """

        self.valid_data: dict = {
            "details": {
                "name": "string",
                "serial_number": "string",
                "uuid": "string"
            },
            "os": {
                "name": "string",
                "version_major": 0,
                "version": "string"
            },
            "software": [
                {
                "name": "string",
                "category": "string",
                "version": "string"
                }
            ]
        }


    def test_serializer_valid_data(self):
        """Serializer Validation Check

        Ensure that if creating an item with valid data it creates
        with no errors
        """

        serializer = InventorySerializer(
            data = self.valid_data
        )


        assert serializer.is_valid(raise_exception = True)



    def test_serializer_valid_data_no_os(self):
        """Serializer Validation Check

        Ensure that if creating an item with valid data that is missing the
        os field, the item is still created
        """

        data = self.valid_data.copy()

        del data['os']

        serializer = InventorySerializer(
            data = data
        )


        assert serializer.is_valid(raise_exception = True)



    def test_serializer_valid_data_empty_software(self):
        """Serializer Validation Check

        Ensure that if creating an item with valid data that has an empty
        software field, the item is still created
        """

        data = self.valid_data.copy()

        data['software'] = []

        serializer = InventorySerializer(
            data = data
        )


        assert serializer.is_valid(raise_exception = True)



    def test_serializer_valid_data_no_software(self):
        """Serializer Validation Check

        Ensure that if creating an item with valid data that is missing the
        software field, the item is still created
        """

        data = self.valid_data.copy()

        del data['software']

        serializer = InventorySerializer(
            data = data
        )


        assert serializer.is_valid(raise_exception = True)



    def test_serializer_valid_data_details_only(self):
        """Serializer Validation Check

        Ensure that if creating an item with valid data that is missing the
        os and software field, the item is still created
        """

        data = self.valid_data.copy()

        del data['os']
        del data['software']

        serializer = InventorySerializer(
            data = data
        )


        assert serializer.is_valid(raise_exception = True)



    def test_serializer_valid_data_details_no_serial(self):
        """Serializer Validation Check

        Ensure that if creating an item with valid data that is missing the
        details.os and software field, the item is still created
        """

        data = self.valid_data.copy()

        del data['details']['serial_number']

        serializer = InventorySerializer(
            data = data
        )


        assert serializer.is_valid(raise_exception = True)



    def test_serializer_valid_data_details_no_uuid(self):
        """Serializer Validation Check

        Ensure that if creating an item with valid data that is missing the
        details.uuid and software field, the item is still created
        """

        data = self.valid_data.copy()

        del data['details']['uuid']

        serializer = InventorySerializer(
            data = data
        )


        assert serializer.is_valid(raise_exception = True)




    def test_serializer_validation_no_serial_and_uuid(self):
        """Serializer Validation Check

        Ensure that if creating and no name is provided a validation error occurs
        """

        data = self.valid_data.copy()

        del data['details']['uuid']
        del data['details']['serial_number']

        with pytest.raises(ValidationError) as err:

            serializer = InventorySerializer(
                data = data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['details']['non_field_errors'][0] == 'no_serial_or_uuid'
