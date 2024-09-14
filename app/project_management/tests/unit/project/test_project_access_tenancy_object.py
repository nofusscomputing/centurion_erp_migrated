import pytest
import unittest
import requests

from django.test import TestCase, Client

from access.tests.abstract.tenancy_object import TenancyObject

from project_management.models.projects import Project



class ProjectTenancyObject(
    TestCase,
    TenancyObject
):

    model = Project
