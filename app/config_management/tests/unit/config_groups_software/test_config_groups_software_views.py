import pytest
import unittest
import requests

from django.test import TestCase

from app.tests.abstract.models import AddView, ChangeView, DeleteView



class ConfigGroupsSoftwareViews(
    TestCase,
    AddView,
    ChangeView,
    DeleteView
):

    add_module = 'config_management.views.groups.software'
    add_view = 'GroupSoftwareAdd'

    change_module = add_module
    change_view = 'GroupSoftwareChange'

    delete_module = add_module
    delete_view = 'GroupSoftwareDelete'

    # display_module = add_module
    # display_view = 'GroupView'

    # index_module = add_module
    # index_view = 'GroupIndexView'
