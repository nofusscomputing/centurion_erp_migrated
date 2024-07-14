import pytest
import unittest
import requests

from django.test import TestCase

from app.tests.abstract.models import ModelDisplay



class HistoryViews(
    TestCase,
    ModelDisplay
):

    # add_module = 'config_management.views.groups.groups'
    # add_view = 'GroupAdd'

    # change_module = add_module
    # change_view = 'GroupView'

    # delete_module = add_module
    # delete_view = 'GroupDelete'

    display_module = 'core.views.history'
    display_view = 'View'

    # index_module = add_module
    # index_view = 'GroupIndexView'

    @pytest.mark.skip(reason="test this models dynamic build of self.model")
    def test_view_display_attribute_exists_model(self):
        """ As part of display init this view dynamically builds self.model """

        pass
