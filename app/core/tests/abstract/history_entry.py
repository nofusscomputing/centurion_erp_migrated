
import pytest
import unittest

from core.models.history import History



class HistoryEntry:


    # field type testing to be done as part of model testing
    def test_history_entry_item_add_field_action(self):
        """ Ensure action is "add" for item creation """

        history = self.history_create.__dict__

        assert history['action'] == int(History.Actions.ADD[0])
        # assert type(history['action']) is int


    @pytest.mark.skip(reason="to be written")
    def test_history_entry_item_add_field_after(self):
        """ Ensure after field contains correct value """

        history = self.history_create.__dict__

        assert history['after'] == str('{}')
        # assert type(history['after']) is str


    def test_history_entry_item_add_field_before(self):
        """ Ensure before field is an empty JSON string for create """

        history = self.history_create.__dict__

        assert history['before'] == str('{}')
        # assert type(history['before']) is str


    def test_history_entry_item_add_field_item_pk(self):
        """ Ensure history entry field item_pk is the created items pk """

        history = self.history_create.__dict__

        assert history['item_pk'] == self.item_create.pk
        # assert type(history['item_pk']) is int


    def test_history_entry_item_add_field_item_class(self):
        """ Ensure history entry field item_class is the model name """

        history = self.history_create.__dict__

        assert history['item_class'] == self.model._meta.model_name
        # assert type(history['item_class']) is str




################################## Change ##################################




    # field type testing to be done as part of model testing
    def test_history_entry_item_change_field_action(self):
        """ Ensure action is "add" for item creation """

        history = self.history_change.__dict__

        assert history['action'] == int(History.Actions.UPDATE[0])
        # assert type(history['action']) is int


    def test_history_entry_item_change_field_after(self):
        """ Ensure after field contains correct value """

        history = self.history_change.__dict__

        assert history['after'] == str(self.field_after_expected_value)
        # assert type(history['after']) is str


    @pytest.mark.skip(reason="to be written")
    def test_history_entry_item_change_field_before(self):
        """ Ensure before field is an empty JSON string for create """

        history = self.history_change.__dict__

        assert history['before'] == str('{}')
        # assert type(history['before']) is str


    def test_history_entry_item_change_field_item_pk(self):
        """ Ensure history entry field item_pk is the created items pk """

        history = self.history_change.__dict__

        assert history['item_pk'] == self.item_create.pk
        # assert type(history['item_pk']) is int


    def test_history_entry_item_change_field_item_class(self):
        """ Ensure history entry field item_class is the model name """

        history = self.history_change.__dict__

        assert history['item_class'] == self.model._meta.model_name
        # assert type(history['item_class']) is str
