import pytest
# import unittest
# import requests

from django.test import TestCase

from app.tests.abstract.models import TenancyModel

from project_management.models.project_types import ProjectType


class ProjectTypeModel(
    TestCase,
    TenancyModel
):

    model = ProjectType


    # def test_attribute_duration_ticket_value(self):
    #     """Attribute value test

    #     This aattribute calculates the ticket duration from
    #     it's comments. must return total time in seconds
    #     """

    #     pass