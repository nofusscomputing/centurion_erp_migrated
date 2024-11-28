import pytest

from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models import Organization

from settings.serializers.external_links import (
    ExternalLink,
    ExternalLinkModelSerializer
)



class ExternalLinkValidationAPI(
    TestCase,
):

    model = ExternalLink

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        2. Create an item
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.valid_data: dict = {
            'organization': self.organization.id,
            'name': 'a name',
            'template': 'http://example.com/{{ val }}'
        }



    def test_serializer_valid_data(self):
        """Serializer Validation Check

        Ensure that if creating an item with valid data that
        no errors occur
        """

        serializer = ExternalLinkModelSerializer(
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

            serializer = ExternalLinkModelSerializer(
                data = data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['name'][0] == 'required'




    def test_serializer_validation_no_template(self):
        """Serializer Validation Check

        Ensure that if creating and no template is provided a validation error occurs
        """

        data = self.valid_data.copy()

        del data['template']

        with pytest.raises(ValidationError) as err:

            serializer = ExternalLinkModelSerializer(
                data = data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['template'][0] == 'required'
