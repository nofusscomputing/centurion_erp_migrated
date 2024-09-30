from django.contrib.auth.models import User
from django.test import TestCase

from access.models import Organization, Team, TeamUsers, Permission

from api.v2.tests.unit.abstract.test_model_unit import ModelAttributesUnit



class Model(
    TestCase,
    ModelAttributesUnit,
):

    model = Organization
