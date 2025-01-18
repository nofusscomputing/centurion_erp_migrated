import pytest

from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models import Organization

from app.tests.abstract.mock_view import MockView, User

from itam.serializers.operating_system_version import OperatingSystem, OperatingSystemVersion, OperatingSystemVersionModelSerializer



class OperatingSystemVersionValidationAPI(
    TestCase,
):

    model = OperatingSystemVersion

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        2. Create an item
        """

        organization = Organization.objects.create(name='test_org')

        self.user = User.objects.create_user(username="test_user_view", password="password")

        self.mock_view = MockView( user = self.user )

        self.organization = organization

        os = OperatingSystem.objects.create(
            organization=organization,
            name = 'os name'
        )

        self.item = self.model.objects.create(
            organization=organization,
            name = 'os name',
            operating_system = os
        )



    def test_serializer_validation_no_name(self):
        """Serializer Validation Check

        Ensure that if creating and no name is provided a validation error occurs
        """

        with pytest.raises(ValidationError) as err:

            serializer = OperatingSystemVersionModelSerializer(
                context = {
                    'request': self.mock_view.request,
                    'view': self.mock_view,
                },
                data={
                "organization": self.organization.id,
            })

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['name'][0] == 'required'
