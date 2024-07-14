import pytest
import unittest
import requests

from django.test import TestCase

from app.tests.abstract.models import AddView, DeleteView



class TeamUserViews(
    TestCase,
    AddView,
    DeleteView
):

    add_module = 'access.views.user'
    add_view = 'Add'

    # change_module = add_module
    # change_view = 'GroupView'

    delete_module = add_module
    delete_view = 'Delete'

    # display_module = add_module
    # display_view = 'GroupView'

    # index_module = add_module
    # index_view = 'GroupIndexView'
