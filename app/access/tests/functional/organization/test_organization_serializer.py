import pytest

from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.serializers.organization import (
    Organization,
    OrganizationModelSerializer
)



class OrganizationValidationAPI(
    TestCase,
):

    model = Organization

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        2. Create an item
        """

        self.user = User.objects.create(username = 'org_user', password='random password')

        self.valid_data = {
            'name': 'valid_org_data',
            'manager': self.user.id
        }

        self.item = self.model.objects.create(
            name = 'random title',
        )



    def test_serializer_valid_data(self):
        """Serializer Validation Check

        Ensure that if creating and no name is provided a validation error occurs
        """

        serializer = OrganizationModelSerializer(
            data = self.valid_data
        )

        assert serializer.is_valid(raise_exception = True)



    def test_serializer_validation_no_name(self):
        """Serializer Validation Check

        Ensure that if creating and no name is provided a validation error occurs
        """

        data = self.valid_data.copy()
        
        del data['name']

        with pytest.raises(ValidationError) as err:

            serializer = OrganizationModelSerializer(
                data = data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['name'][0] == 'required'



    def test_serializer_validation_manager_optional(self):
        """Serializer Validation Check

        Ensure that if creating and no name is provided a validation error occurs
        """

        data = self.valid_data.copy()
        
        del data['manager']

        serializer = OrganizationModelSerializer(
            data = data
        )

        assert serializer.is_valid(raise_exception = True)
