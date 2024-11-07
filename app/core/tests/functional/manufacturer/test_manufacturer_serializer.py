import pytest

from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models import Organization

from core.serializers.manufacturer import Manufacturer, ManufacturerModelSerializer



class ManufacturerValidationAPI(
    TestCase,
):

    model = Manufacturer

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
            name = 'random title',
        )



    def test_serializer_validation_no_name(self):
        """Serializer Validation Check

        Ensure that if creating and no name is provided a validation error occurs
        """

        with pytest.raises(ValidationError) as err:

            serializer = ManufacturerModelSerializer(data={
                "organization": self.organization.id,
            })

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['name'][0] == 'required'



    def test_serializer_validation_add_existing_manufacturer(self):
        """Serializer Validation Check

        Ensure that if adding the same manufacturer
        it raises a validation error
        """

        with pytest.raises(ValidationError) as err:

            serializer = ManufacturerModelSerializer(
                data={
                    "organization": self.organization.id,
                    "name": self.item.name
                }
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['name'][0] == 'unique'
