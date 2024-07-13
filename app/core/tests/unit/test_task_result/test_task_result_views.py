import pytest
import unittest
import requests

from django.test import TestCase

from app.tests.abstract.models import ModelDisplay, ModelIndex



class TaskResultsViews(
    TestCase,
    ModelDisplay,
    ModelIndex
):

    # add_module = 'core.views.celery_log'
    # add_view = 'GroupAdd'

    # change_module = add_module
    # change_view = 'GroupView'

    # delete_module = add_module
    # delete_view = 'GroupDelete'

    display_module = 'core.views.celery_log'
    display_view = 'View'

    index_module = display_module
    index_view = 'Index'
