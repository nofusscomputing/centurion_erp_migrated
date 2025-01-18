import json
import pytest

from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models import Organization, Team

from app.tests.abstract.mock_view import MockView, User

from assistance.serializers.knowledge_base_category import KnowledgeBaseCategory, KnowledgeBaseCategoryModelSerializer



class KnowledgeBaseCategoryValidationAPI(
    TestCase,
):

    model = KnowledgeBaseCategory

    app_namespace = 'API'
    
    url_name = '_api_v2_knowledge_base'

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        2. Create a team
        4. Add user to add team
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.add_team = Team.objects.create(
            organization=organization,
            team_name = 'teamone',
            model_notes = 'random note'
        )

        self.add_user = User.objects.create_user(username="test_user_add", password="password")

        self.mock_view = MockView( user = self.add_user )

        self.item_has_target_user = self.model.objects.create(
            organization=organization,
            name = 'random title',
            target_user = self.add_user,
        )

        self.item_has_target_team = self.model.objects.create(
            organization=organization,
            name = 'random title0',
        )

        self.item_has_target_team.target_team.set([ self.add_team ])



    def test_serializer_validation_no_name(self):
        """Serializer Validation Check

        Ensure that if creating and no name is provided a validation error occurs
        """

        with pytest.raises(ValidationError) as err:

            serializer = KnowledgeBaseCategoryModelSerializer(
                context = {
                    'request': self.mock_view.request,
                    'view': self.mock_view,
                },
                data={
                    "organization": self.organization.id,
                    "target_user": self.add_user.id,
                    "target_team": [
                        self.add_team.id
                    ]
            })

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['name'][0] == 'required'



    def test_serializer_validation_parent_category_not_self(self):
        """Serializer Validation Check

        Ensure that you cant assisgn self as parent category
        """

        with pytest.raises(ValidationError) as err:

            serializer = KnowledgeBaseCategoryModelSerializer(
                self.item_has_target_user,
                context = {
                    'request': self.mock_view.request,
                    'view': self.mock_view,
                },
                data={
                    "parent_category": self.item_has_target_user.id
                },
                partial=True,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['parent_category'][0] == 'parent_category_not_self'



    def test_serializer_validation_both_target_team_target_user(self):
        """Serializer Validation Check

        Ensure that both target user and target team raises a validation error
        """

        with pytest.raises(ValidationError) as err:

            serializer = KnowledgeBaseCategoryModelSerializer(
                context = {
                    'request': self.mock_view.request,
                    'view': self.mock_view,
                },
                data={
                    "organization": self.organization.id,
                    "name": "teamone",
                    "target_user": self.add_user.id,
                    "target_team": [
                        self.add_team.id
                    ]
            })

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['non_field_errors'][0] == 'invalid_not_both_target_team_user'



    def test_serializer_validation_no_target_team_target_user(self):
        """Serializer Validation Check

        Ensure that if either target user and target team is missing it raises validation error
        """

        with pytest.raises(ValidationError) as err:

            serializer = KnowledgeBaseCategoryModelSerializer(
                context = {
                    'request': self.mock_view.request,
                    'view': self.mock_view,
                },
                data={
                "organization": self.organization.id,
                "name": 'teamone' 
            })

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['non_field_errors'][0] == 'invalid_need_target_team_or_user'



    def test_serializer_validation_update_existing_target_user(self):
        """Serializer Validation Check

        Ensure that if an existing item with target user is updated to include a target_team
        it raises a validation error
        """

        with pytest.raises(ValidationError) as err:

            serializer = KnowledgeBaseCategoryModelSerializer(
                self.item_has_target_user,
                context = {
                    'request': self.mock_view.request,
                    'view': self.mock_view,
                },
                data={
                    "target_team": [ self.add_team.id ]
                },
                partial=True,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['non_field_errors'][0] == 'invalid_not_both_target_team_user'


    def test_serializer_validation_update_existing_target_team(self):
        """Serializer Validation Check

        Ensure that if an existing item with target team is updated to include a target_user
        it raises a validation error
        """

        with pytest.raises(ValidationError) as err:

            serializer = KnowledgeBaseCategoryModelSerializer(
                self.item_has_target_team,
                context = {
                    'request': self.mock_view.request,
                    'view': self.mock_view,
                },
                data={
                    "target_user": self.add_user.id
                },
                partial=True,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['non_field_errors'][0] == 'invalid_not_both_target_team_user'
