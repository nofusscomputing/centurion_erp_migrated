import pytest
import unittest

from django.test import TestCase

from access.models import Organization

from app.tests.abstract.models import TenancyModel

from assistance.models.knowledge_base import KnowledgeBase



@pytest.mark.django_db
class KnowledgeBaseModel(
    TestCase,
    TenancyModel
):

    model = KnowledgeBase

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create an item

        """

        self.organization = Organization.objects.create(name='test_org')


        self.item = self.model.objects.create(
            organization = self.organization,
            title = 'one',
            content = 'dict({"key": "one", "existing": "dont_over_write"})'
        )

        self.second_item = self.model.objects.create(
            organization = self.organization,
            title = 'one_two',
            content = 'dict({"key": "two"})',
        )
