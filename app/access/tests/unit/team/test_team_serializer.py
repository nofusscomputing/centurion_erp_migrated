import pytest

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models import Organization, Permission

from access.serializers.teams import (
    Team,
    TeamModelSerializer
)



class MockView:

    action: str = None

    kwargs: dict = {}



class MockRequest:

    user = None



class TeamValidationAPI(
    TestCase,
):

    model = Team

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        2. Create an item
        """

        self.organization = Organization.objects.create(
            name = 'team org serializer test'
        )

        self.user = User.objects.create(username = 'org_user', password='random password')


        view_permissions = Permission.objects.get(
                codename = 'view_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )


        self.valid_data = {
            'organization': self.organization.id,
            'team_name': 'valid_org_data',
            'permissions': [
                view_permissions.id,
            ]
        }

        self.item = self.model.objects.create(
            organization = self.organization,
            name = 'random team title',
        )



    def test_serializer_valid_data(self):
        """Serializer Validation Check

        Ensure that if creating an item supplied valid data
        creates an item.
        """


        mock_view = MockView()
        mock_view.action = 'create'
        mock_view.kwargs: dict = {
            'organization_id': self.organization.id
        }

        mock_request = MockRequest()
        mock_request.user = self.user

        mock_view.request = mock_request


        serializer = TeamModelSerializer(
            context = {
                'request': mock_request,
                'view': mock_view,
            },
            data = self.valid_data
        )

        assert serializer.is_valid(raise_exception = True)



    def test_serializer_validation_no_name(self):
        """Serializer Validation Check

        Ensure that if creating and no name is provided a validation error occurs
        """


        mock_view = MockView()
        mock_view.action = 'create'
        mock_view.kwargs: dict = {
            'organization_id': self.organization.id
        }

        mock_request = MockRequest()
        mock_request.user = self.user

        mock_view.request = mock_request


        data = self.valid_data.copy()
        
        del data['team_name']

        with pytest.raises(ValidationError) as err:

            serializer = TeamModelSerializer(
                context = {
                    'request': mock_request,
                    'view': mock_view,
                },
                data = data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['team_name'][0] == 'required'



    def test_serializer_validation_permissions_optional(self):
        """Serializer Validation Check

        Ensure that if creating and permissions are not supplied, the item is 
        still created.
        """


        mock_view = MockView()
        mock_view.action = 'create'
        mock_view.kwargs: dict = {
            'organization_id': self.organization.id
        }

        mock_request = MockRequest()
        mock_request.user = self.user

        mock_view.request = mock_request


        data = self.valid_data.copy()
        
        del data['permissions']

        serializer = TeamModelSerializer(
            context = {
                'request': mock_request,
                'view': mock_view,
            },
            data = data
        )

        assert serializer.is_valid(raise_exception = True)
