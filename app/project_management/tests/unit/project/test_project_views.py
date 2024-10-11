import pytest
import unittest
import requests

from django.test import TestCase

from app.tests.abstract.models import PrimaryModel, ModelAdd, ModelChange, ModelDelete



# class TicketCommentViews(
#     TestCase,
#     PrimaryModel
# ):
class ProjectViews(
    TestCase,
    PrimaryModel
):

    add_module = 'project_management.views.project'
    add_view = 'Add'

    change_module = add_module
    change_view = 'Change'

    delete_module = add_module
    delete_view = 'Delete'

    display_module = add_module
    display_view = 'View'

    index_module = add_module
    index_view = 'Index'
