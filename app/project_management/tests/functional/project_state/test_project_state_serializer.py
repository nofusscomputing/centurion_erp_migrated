import pytest

from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models import Organization

from app.tests.abstract.mock_view import MockView, User

from project_management.serializers.project_states import (
    ProjectState,
    ProjectStateModelSerializer
)



class ProjectStateValidationAPI(
    TestCase,
):

    model = ProjectState

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        2. Create an item
        """

        organization = Organization.objects.create(name='test_org')

        self.user = User.objects.create_user(username="test_user_view", password="password")

        self.organization = organization

        self.mock_view = MockView( user = self.user )



    def test_serializer_validation_can_create(self):
        """Serializer Validation Check

        Ensure that a valid item can be creates
        """

        serializer = ProjectStateModelSerializer(
            context = {
                'request': self.mock_view.request,
                'view': self.mock_view,
            },
            data={
                "organization": self.organization.id,
                "name": 'a project'
            }
        )

        assert serializer.is_valid(raise_exception = True)



    def test_serializer_validation_no_name(self):
        """Serializer Validation Check

        Ensure that if creating and no name is provided a validation error occurs
        """

        with pytest.raises(ValidationError) as err:

            serializer = ProjectStateModelSerializer(
                context = {
                    'request': self.mock_view.request,
                    'view': self.mock_view,
                },
                data={
                    "organization": self.organization.id,
                },
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['name'][0] == 'required'
