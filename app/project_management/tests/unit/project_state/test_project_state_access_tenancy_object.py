import pytest

from django.test import TestCase

from access.tests.abstract.tenancy_object import TenancyObject

from project_management.models.project_states import ProjectState



class ProjectStateTenancyObject(
    TestCase,
    TenancyObject
):

    model = ProjectState
