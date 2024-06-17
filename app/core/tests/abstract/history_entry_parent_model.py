
import pytest
import unittest

from core.models.history import History



class HistoryEntryParentItem:


    def test_history_entry_delete(self):
        """ When an item is deleted, it's history entries must be removed """

        assert self.history_delete.exists() is False


    def test_history_entry_children_delete(self):
        """ When an item is deleted, it's history entries must be removed """

        assert self.history_delete_children.exists() is False
