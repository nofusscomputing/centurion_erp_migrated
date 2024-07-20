import pytest
import unittest

from django.test import TestCase

from access.models import Organization

from app.tests.abstract.models import TenancyModel

from assistance.models.knowledge_base import KnowledgeBaseCategory



@pytest.mark.django_db
class KnowledgeBaseModel(
    TestCase,
    TenancyModel
):

    model = KnowledgeBaseCategory

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create an item

        """

        self.organization = Organization.objects.create(name='test_org')


        self.item = self.model.objects.create(
            organization = self.organization,
            name = 'one',
        )

        self.second_item = self.model.objects.create(
            organization = self.organization,
            name = 'one_two',
        )
