import pytest

from django.test import TestCase

from access.tests.abstract.tenancy_object import TenancyObject

from project_management.models.project_types import ProjectType



class ProjectTypeTenancyObject(
    TestCase,
    TenancyObject
):

    model = ProjectType
