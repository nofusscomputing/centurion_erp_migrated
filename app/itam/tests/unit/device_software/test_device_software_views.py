import pytest
import unittest
import requests

from django.test import TestCase

from app.tests.abstract.models import ModelAdd, ModelChange, ModelDisplay



class DeviceSoftwareViews(
    TestCase,
    ModelAdd,
    ModelChange,
    ModelDisplay
):

    add_module = 'itam.views.device'
    add_view = 'SoftwareAdd'

    change_module = add_module
    change_view = 'SoftwareView'

    # delete_module = add_module
    # delete_view = 'Delete'

    display_module = add_module
    display_view = 'SoftwareView'
