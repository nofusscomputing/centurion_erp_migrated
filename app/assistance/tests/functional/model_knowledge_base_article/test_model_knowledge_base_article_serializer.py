import json
import pytest

from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models import Organization, Team

from assistance.models.model_knowledge_base_article import KnowledgeBase, ModelKnowledgeBaseArticle
from assistance.serializers.model_knowledge_base_article import ModelKnowledgeBaseArticleModelSerializer

from itam.models.device import Device



class MockView:

    action: str = None

    kwargs: dict = {}



class KnowledgeBaseValidationAPI(
    TestCase,
):

    model = ModelKnowledgeBaseArticle

    app_namespace = 'API'
    
    url_name = '_api_v2_model_kb'

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        2. Create a team
        4. Add user to add team
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.knowledge_base = KnowledgeBase.objects.create(
            organization = self.organization,
            title = 'title',
            content = 'sdfsdf'
        )

        self.device = Device.objects.create(
            organization = self.organization,
            name = 'device'
        )

        self.add_user = User.objects.create_user(username="test_user_add", password="password")

        self.valid_data: dict = {
            'article': self.knowledge_base.id,
        }



    def test_serializer_valid_data(self):
        """Serializer Validation Check

        Ensure that if creating with valid data that
        no validation error occurs
        """

        mock_view = MockView()

        mock_view.kwargs = {
            'model': 'device',
            'model_pk': self.device.id
        }

        mock_view.action = 'create'

        serializer = ModelKnowledgeBaseArticleModelSerializer(
            context = {
                'view': mock_view
            },
            data = self.valid_data,
        )


        assert serializer.is_valid(raise_exception = True)



    def test_serializer_validation_no_article_supplied(self):
        """Serializer Validation Check

        Ensure if no article is supplied a validation error is raised
        """

        mock_view = MockView()

        mock_view.kwargs = {
            'model': 'device',
            'model_pk': self.device.id
        }

        mock_view.action = 'create'

        data = self.valid_data.copy()

        del data['article']

        with pytest.raises(ValidationError) as err:

            serializer = ModelKnowledgeBaseArticleModelSerializer(
                context = {
                    'view': mock_view
                },
                data = data,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['article'][0] == 'required'



    def test_serializer_validation_no_model_pk_supplied(self):
        """Serializer Validation Check

        Ensure if no model is not supplied a validation error is raised
        """

        mock_view = MockView()

        mock_view.kwargs = {
            'model': 'device',
        }

        mock_view.action = 'create'

        data = self.valid_data.copy()

        with pytest.raises(ValidationError) as err:

            serializer = ModelKnowledgeBaseArticleModelSerializer(
                context = {
                    'view': mock_view
                },
                data = data,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()[0] == 'model_details_required'



    def test_serializer_validation_no_model_supplied(self):
        """Serializer Validation Check

        Ensure if no model_pk is not supplied a validation error is raised
        """

        mock_view = MockView()

        mock_view.kwargs = {
            'model_pk': self.device.id
        }

        mock_view.action = 'create'

        data = self.valid_data.copy()

        with pytest.raises(ValidationError) as err:

            serializer = ModelKnowledgeBaseArticleModelSerializer(
                context = {
                    'view': mock_view
                },
                data = data,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()[0] == 'model_details_required'



    def test_serializer_validation_no_model_fields_supplied(self):
        """Serializer Validation Check

        Ensure if model and model_pk is not supplied a validation error is raised
        """

        mock_view = MockView()

        mock_view.kwargs = {}

        mock_view.action = 'create'

        data = self.valid_data.copy()

        with pytest.raises(ValidationError) as err:

            serializer = ModelKnowledgeBaseArticleModelSerializer(
                context = {
                    'view': mock_view
                },
                data = data,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()[0] == 'model_details_required'
