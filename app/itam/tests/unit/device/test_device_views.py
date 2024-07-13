import pytest
import unittest
import requests

from django.test import TestCase

from app.tests.abstract.models import PrimaryModel


class DeviceViews(
    TestCase,
    PrimaryModel
):

    add_module = 'itam.views.device'
    add_view = 'Add'

    change_module = 'itam.views.device'
    change_view = 'Change'

    delete_module = 'itam.views.device'
    delete_view = 'Delete'

    display_module = 'itam.views.device'
    display_view = 'View'

    index_module = 'itam.views.device'
    index_view = 'IndexView'
