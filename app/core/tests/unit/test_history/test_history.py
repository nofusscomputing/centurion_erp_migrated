
from django.test import TestCase, Client

import pytest
import unittest
import requests

from core.models.history import History

class History(TestCase):


    model = History


    @pytest.mark.skip(reason="to be written")
    def test_history_auth_view_super_admin():
        """ Super Admin can view history without requiring permission """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_history_no_entry_without_item():
        """ A history entry cant be created without an item

        fields required `item_pk` and `item_class`
        """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_history_no_entry_without_parent_item():
        """ A history entry cant be created without a parent item

        fields required `parent_item_pk` and `parent_item_class
        """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_history_save_calls_save_history():
        """ During model save, self.save_history is called

        This method saves the history to the database
        """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_history_delete_calls_save_history():
        """ During model delete, self.save_history is called

        This method saves the delete history to the database for parent objects
        """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_history_delete_calls_delete_history():
        """ During model delete, self.delete_history is called

        This method deletes the item and child-item history from the database
        """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_function_save_attributes():
        """ Ensure save Attributes function match django default

        the save method is overridden. the function attributes must match default django method
        """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_function_delete_attributes():
        """ Ensure delete Attributes function match django default

        the delete method is overridden. the function attributes must match default django method
        """
        pass
