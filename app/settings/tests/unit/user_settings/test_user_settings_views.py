import pytest
import unittest
import requests

from django.test import TestCase

from app.tests.abstract.models import ModelChange, ModelDisplay



class AppSettingsViews(
    TestCase,
    ModelChange,
    ModelDisplay
):

    # add_module = 'itam.views.software'
    # add_view = 'Add'

    change_module = 'settings.views.user_settings'
    change_view = 'Change'

    # delete_module = add_module
    # delete_view = 'Delete'

    display_module = change_module
    display_view = 'View'

    # index_module = 'settings.views.software_categories'
    # index_view = 'Index'


    @pytest.mark.skip(reason = "write test to check perms")
    def test_view_change_attribute_exists_permission_required(self):
        """ Test not required as permission check is different """

        pass


    @pytest.mark.skip(reason = "write test to check perms")
    def test_view_change_attribute_type_permission_required(self):
        """ Test not required as permission check is different """

        pass
