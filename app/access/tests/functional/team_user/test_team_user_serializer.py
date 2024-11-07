import pytest

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models import Organization, Permission, Team

from access.serializers.team_user import (
    TeamUsers,
    TeamUserModelSerializer
)



class MockView:

    action: str = None

    kwargs: dict = {}



class MockRequest:

    user = None



class TeamValidationAPI(
    TestCase,
):

    model = TeamUsers

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

        self.team = Team.objects.create(
            organization = self.organization,
            name = 'random team title',
        )


        self.valid_data = {
            'team': self.team.id,
            'user': self.user.id
        }


        self.item = self.model.objects.create(
            team = self.team,
            user = self.user,
        )



    def test_serializer_valid_data(self):
        """Serializer Validation Check

        Ensure that if creating an item supplied valid data
        creates an item.
        """


        mock_view = MockView()
        mock_view.action = 'create'
        mock_view.kwargs: dict = {
            'organization_id': self.organization.id,
            'team_id': self.team.id
        }

        mock_request = MockRequest()
        mock_request.user = self.user

        mock_view.request = mock_request


        serializer = TeamUserModelSerializer(
            context = {
                'request': mock_request,
                'view': mock_view,
            },
            data = self.valid_data
        )

        assert serializer.is_valid(raise_exception = True)



    def test_serializer_validation_no_team_creates(self):
        """Serializer Validation Check

        Ensure that if creating and no team is provided no validation
        error occurs as the team id is collected from the view
        """


        mock_view = MockView()
        mock_view.action = 'create'
        mock_view.kwargs: dict = {
            'organization_id': self.organization.id,
            'team_id': self.team.id
        }

        mock_request = MockRequest()
        mock_request.user = self.user

        mock_view.request = mock_request


        data = self.valid_data.copy()
        
        del data['team']

        serializer = TeamUserModelSerializer(
            context = {
                'request': mock_request,
                'view': mock_view,
            },
            data = data
        )

        assert serializer.is_valid(raise_exception = True)



    def test_serializer_validation_no_user(self):
        """Serializer Validation Check

        Ensure that if creating and no user is provided a validation error occurs
        """


        mock_view = MockView()
        mock_view.action = 'create'
        mock_view.kwargs: dict = {
            'organization_id': self.organization.id,
            'team_id': self.team.id
        }

        mock_request = MockRequest()
        mock_request.user = self.user

        mock_view.request = mock_request


        data = self.valid_data.copy()
        
        del data['user']

        with pytest.raises(ValidationError) as err:

            serializer = TeamUserModelSerializer(
                context = {
                    'request': mock_request,
                    'view': mock_view,
                },
                data = data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['user'][0] == 'required'
