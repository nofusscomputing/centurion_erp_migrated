import pytest
# import unittest
# import requests

from django.test import TestCase

from app.tests.abstract.models import TenancyModel

from project_management.models.projects import Project


class ProjectModel(
    TestCase,
    TenancyModel
):

    model = Project


    # def test_attribute_duration_ticket_value(self):
    #     """Attribute value test

    #     This aattribute calculates the ticket duration from
    #     it's comments. must return total time in seconds
    #     """

    #     pass