
import pytest
import unittest
import requests

from django.test import TestCase, Client

from access.models import Organization

from core.models.history import History
from core.tests.abstract.history_entry import HistoryEntry
from core.tests.abstract.history_entry_parent_model import HistoryEntryParentItem

from assistance.models.knowledge_base import KnowledgeBaseCategory



class KnowledgeBaseHistory(TestCase, HistoryEntry, HistoryEntryParentItem):


    model = KnowledgeBaseCategory


    @classmethod
    def setUpTestData(self):
        """ Setup Test """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization


        self.item_create = self.model.objects.create(
            name = 'test_item_' + self.model._meta.model_name,
            organization = self.organization,
        )


        self.history_create = History.objects.get(
            action = History.Actions.ADD[0],
            item_pk = self.item_create.pk,
            item_class = self.model._meta.model_name,
        )

        self.item_change = self.item_create
        self.item_change.name = 'test_item_' + self.model._meta.model_name + '_changed'
        self.item_change.save()

        self.field_after_expected_value = '{"name": "' + self.item_change.name + '"}'

        self.history_change = History.objects.get(
            action = History.Actions.UPDATE[0],
            item_pk = self.item_change.pk,
            item_class = self.model._meta.model_name,
        )

        self.item_delete = self.model.objects.create(
            name = 'test_item_delete_' + self.model._meta.model_name,
            organization = self.organization,
        )

        self.deleted_pk = self.item_delete.pk

        self.item_delete.delete()

        self.history_delete = History.objects.filter(
            item_pk = self.deleted_pk,
            item_class = self.model._meta.model_name,
        )


    def test_history_entry_children_delete(self):
        """ Model has no child items """
        pass

