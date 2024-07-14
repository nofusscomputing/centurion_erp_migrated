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

    change_module = 'settings.views.app_settings'
    change_view = 'View'

    # delete_module = add_module
    # delete_view = 'Delete'

    display_module = change_module
    display_view = change_view

    # index_module = 'settings.views.software_categories'
    # index_view = 'Index'
