import pytest
import unittest
import requests

from django.test import TestCase

from app.tests.abstract.models import ModelAdd, ModelDelete, ModelDisplay



class TeamViews(
    TestCase,
    ModelAdd,
    ModelDelete,
    ModelDisplay,
):

    add_module = 'access.views.team'
    add_view = 'Add'

    # change_module = add_module
    # change_view = 'Change'

    delete_module = add_module
    delete_view = 'Delete'

    display_module = add_module
    display_view = 'View'

