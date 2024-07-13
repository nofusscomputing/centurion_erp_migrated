import pytest
import unittest
import requests

from django.test import TestCase

from app.tests.abstract.models import PrimaryModel



class ConfigManagementViews(
    TestCase,
    PrimaryModel
):

    add_module = 'config_management.views.groups.groups'
    add_view = 'GroupAdd'

    change_module = add_module
    change_view = 'GroupView'

    delete_module = add_module
    delete_view = 'GroupDelete'

    display_module = add_module
    display_view = 'GroupView'

    index_module = add_module
    index_view = 'GroupIndexView'
