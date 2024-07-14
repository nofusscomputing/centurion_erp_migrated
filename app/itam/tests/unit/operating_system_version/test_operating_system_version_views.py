import pytest
import unittest
import requests

from django.test import TestCase

from app.tests.abstract.models import ModelAdd, ModelChange, ModelDelete, ModelDisplay



class OperatingSystemVersionViews(
    TestCase,
    ModelAdd,
    ModelChange,
    ModelDelete,
    ModelDisplay
):

    add_module = 'itam.views.operating_system_version'
    add_view = 'Add'

    change_module = add_module
    change_view = 'View'

    delete_module = add_module
    delete_view = 'Delete'

    display_module = add_module
    display_view = 'View'

    # index_module = 'settings.views.device_models'
    # index_view = 'Index'
