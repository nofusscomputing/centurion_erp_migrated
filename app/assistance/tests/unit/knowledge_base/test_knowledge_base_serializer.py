import json
import pytest

from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models import Organization, Team

from assistance.models.knowledge_base import KnowledgeBase
from assistance.serializers.knowledge_base import KnowledgeBaseModelSerializer



class KnowledgeBaseValidationAPI(
    TestCase,
):

    model = KnowledgeBase

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

        self.item_has_target_user = self.model.objects.create(
            organization=organization,
            title = 'random title',
            content = 'random note',
            summary = 'a summary',
            target_user = self.add_user,
            release_date = '2024-01-01 12:00:00',
            expiry_date = '2024-01-01 12:00:01',
            responsible_user = self.add_user,
        )

        self.item_has_target_team = self.model.objects.create(
            organization=organization,
            title = 'random title',
            content = 'random note',
            summary = 'a summary',
            release_date = '2024-01-01 12:00:00',
            expiry_date = '2024-01-01 12:00:01',
            responsible_user = self.add_user,
        )

        self.item_has_target_team.target_team.set([ self.add_team ])



    def test_serializer_validation_no_title(self):

        with pytest.raises(ValidationError) as err:

            serializer = KnowledgeBaseModelSerializer(data={
                "organization": self.organization.id,
                "content": "random note",
                "target_user": self.add_user.id,
                "target_team": [
                    self.add_team.id
                ],
                "responsible_user": self.add_user.id,
            })

            serializer.is_valid()

        assert err.value.get_codes()['title'][0] == 'required'



    def test_serializer_validation_both_target_team_target_user(self):

        with pytest.raises(ValidationError) as err:

            serializer = KnowledgeBaseModelSerializer(data={
                "organization": self.organization.id,
                "title": "teamone",
                "content": "random note",
                "target_user": self.add_user.id,
                "target_team": [
                    self.add_team.id
                ],
                "responsible_user": self.add_user.id,
            })

            serializer.is_valid()

        assert err.value.get_codes()['non_field_errors'][0] == 'invalid_not_both_target_team_user'



    def test_serializer_validation_no_target_team_target_user(self):


        with pytest.raises(ValidationError) as err:

            serializer = KnowledgeBaseModelSerializer(data={
                "organization": self.organization.id,
                "title": 'teamone',
                "content": 'random note',
                "responsible_user": self.add_user.id,
            })

            serializer.is_valid()

        assert err.value.get_codes()['non_field_errors'][0] == 'invalid_need_target_team_or_user'



    def test_serializer_validation_update_existing_target_user(self):

        with pytest.raises(ValidationError) as err:

            serializer = KnowledgeBaseModelSerializer(
                self.item_has_target_user,
                data={
                    "target_team": [ self.add_team.id ]
                },
                partial=True,
            )

            serializer.is_valid()

        assert err.value.get_codes()['non_field_errors'][0] == 'invalid_not_both_target_team_user'


    def test_serializer_validation_update_existing_target_team(self):

        with pytest.raises(ValidationError) as err:

            serializer = KnowledgeBaseModelSerializer(
                self.item_has_target_team,
                data={
                    "target_user": self.add_user.id
                },
                partial=True,
            )

            serializer.is_valid()

        assert err.value.get_codes()['non_field_errors'][0] == 'invalid_not_both_target_team_user'