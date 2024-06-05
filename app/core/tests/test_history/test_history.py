
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
