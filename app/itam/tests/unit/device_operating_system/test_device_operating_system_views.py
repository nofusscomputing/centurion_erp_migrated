import pytest
import unittest
import requests

from django.test import TestCase

from app.tests.abstract.models import PrimaryModel



class DeviceOperatingSystemViews(
    TestCase,
    # PrimaryModel
):

    add_module = 'itam.views.device_model'
    add_view = 'Add'

    change_module = add_module
    change_view = 'View'

    delete_module = add_module
    delete_view = 'Delete'

    display_module = add_module
    display_view = 'View'

    index_module = 'settings.views.device_models'
    index_view = 'Index'


    @pytest.mark.skip(reason="refactor moddel views to proper CRUD views")
    def test_dummy(self):

        pass