from django.test import TestCase

import pytest
import requests
import unittest

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from access.models import Organization, Team


# @pytest.fixture
# def organization() -> Organization:
#     return Organization.objects.create(
#         name='Test org',
#     )


# @pytest.fixture
# def team() -> Team:
#     return Team.objects.create(
#         name='Team one',
#         organization = Organization.objects.create(
#             name='Test org',
#         ),
#     )


@pytest.mark.skip(reason="to be written")
def test_authorization_user_permission_add_team_manager(user):
    """Ensure user can be added when user is team manager

        user requires permissions team view and user add
    """
    pass


@pytest.mark.skip(reason="to be written")
def test_authorization_user_permission_delete_team_manager(user):
    """Ensure user can be deleted when user is team manager

        user requires permissions team view and user delete
    """
    pass


# is_superuser to be able to view, add, change, delete for all objects

