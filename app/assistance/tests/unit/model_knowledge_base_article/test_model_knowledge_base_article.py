import pytest
import unittest

from django.test import TestCase

from access.models import Organization

from app.tests.abstract.models import TenancyModel

from assistance.models.model_knowledge_base_article import KnowledgeBase, ModelKnowledgeBaseArticle

from itam.models.device import Device



@pytest.mark.django_db
class ModelKnowledgeBaseArticleModel(
    TestCase,
    TenancyModel
):

    model = ModelKnowledgeBaseArticle

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create an item

        """

        self.organization = Organization.objects.create(name='test_org')

        self.organization_two = Organization.objects.create(name='test_org_two')

        knowledge_base = KnowledgeBase.objects.create(
            organization = self.organization_two,
            title = 'title',
            content = 'sdfsdf'
        )

        knowledge_base_two = KnowledgeBase.objects.create(
            organization = self.organization_two,
            title = 'title two',
            content = 'sdfsdf'
        )

        self.device = Device.objects.create(
            organization = self.organization,
            name = 'device'
        )


        self.item = self.model.objects.create(
            article = knowledge_base,
            model = str( self.device._meta.app_label ) + '.' + str( self.device._meta.model_name ),
            model_pk = self.device.id
        )

        self.second_item = self.model.objects.create(
            article = knowledge_base_two,
            model = str( self.device._meta.app_label ) + '.' + str( self.device._meta.model_name ),
            model_pk = self.device.id
        )



    def test_model_org_matches_model_org(self):
        """Test model clean function

        When an item is created, no org is supplied. The clean
        method within the model is responsible for setting the org
        to match the models org.
        """

        assert self.item.organization.id == self.device.organization.id



    def test_attribute_type_get_url(self):
        """Test field `<model>`type

        This testcase is a duplicate of a test with the same name.

        This model does not use nor require the `get_url` function.

        Attribute `get_url` must be str
        """

        assert type(self.item.get_url()) is not str


    def test_attribute_not_empty_get_url(self):
        """Test field `<model>` is not empty

        This testcase is a duplicate of a test with the same name.

        This model does not use nor require the `get_url` function.

        Attribute `get_url` must contain values
        """

        assert self.item.get_url() is None

