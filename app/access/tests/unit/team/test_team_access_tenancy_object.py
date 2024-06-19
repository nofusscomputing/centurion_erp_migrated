import pytest
import unittest
import requests

from django.test import TestCase, Client

from access.models import Team
from access.tests.abstract.tenancy_object import TenancyObject



class TeamTenancyObject(
    TestCase,
    TenancyObject
):

    model = Team
