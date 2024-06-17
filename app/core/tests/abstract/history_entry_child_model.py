
import pytest
import unittest

from core.models.history import History



class HistoryEntryChildItem:



    def test_history_entry_item_delete_children_entries_not_exist(self):
        """ When an item is deleted, it's children history entries must be removed """

        assert self.history_delete_children.exists() is False


    def test_history_entry_item_delete_field_action(self):
        """ Ensure action is "add" for item creation """

        history = self.history_delete.__dict__

        assert history['action'] == int(History.Actions.DELETE[0])
        # assert type(history['action']) is int


    def test_history_entry_item_delete_field_after(self):
        """ Ensure after field contains correct value """

        history = self.history_delete.__dict__

        assert history['after'] == None
        # assert type(history['after']) is str


    @pytest.mark.skip(reason="figure out best way to test")
    def test_history_entry_item_delete_field_before(self):
        """ Ensure before field is an empty JSON string for create """

        history = self.history_delete.__dict__

        assert history['before'] == str('{}')
        # assert type(history['before']) is str


    def test_history_entry_item_delete_field_item_pk(self):
        """ Ensure history entry field item_pk is the created items pk """

        history = self.history_delete.__dict__

        assert history['item_pk'] == self.deleted_pk
        # assert type(history['item_pk']) is int


    def test_history_entry_item_delete_item_class(self):
        """ Ensure history entry field item_class is the model name """

        history = self.history_delete.__dict__

        assert history['item_class'] == self.model._meta.model_name
        # assert type(history['item_class']) is str



    def test_history_entry_item_delete_field_parent_pk(self):
        """ Ensure history entry field item_pk is the created parents pk """

        history = self.history_delete.__dict__

        assert history['item_parent_pk'] == self.item_parent.pk
        # assert type(history['item_pk']) is int


    def test_history_entry_item_delete_field_parent_class(self):
        """ Ensure history entry field parent_class is the model name """

        history = self.history_delete.__dict__

        assert history['item_parent_class'] == self.item_parent._meta.model_name
        # assert type(history['item_class']) is str

