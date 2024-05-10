from django.conf import settings
from django.shortcuts import reverse
from django.test import TestCase, Client

import pytest
import unittest
import requests

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from structure.models import Organization

# class Test_app_structure_auth(unittest.TestCase):
User = get_user_model()


@pytest.fixture
def user() -> User:
    return User.objects.create_user(username="testuser", password="testpassword")


# @pytest.fixture
# def organization() -> Organization:
#     return Organization.objects.create(
#         name='Test org',
#     )


@pytest.mark.django_db
def test_require_login_organizations():
    """Some docstring defining what the test is checking."""
    client = Client()
    url = reverse('Structure:Organizations')

    response = client.get(url)

    assert response.status_code == 302


@pytest.mark.django_db
def test_require_login_organization_pk():
    """Some docstring defining what the test is checking."""
    client = Client()
    url = reverse('Structure:_singleorg', kwargs={'pk': 1})

    response = client.get(url)

    assert response.status_code == 302


@pytest.mark.django_db
def test_login_view_organizations_no_permission(user):
    """Some docstring defining what the test is checking."""
    client = Client()
    url = reverse('Structure:Organizations')
    client.force_login(user)

    response = client.get(url)

    assert response.status_code == 403


@pytest.mark.skip(reason="to be written")
def test_organizations_permission_change(user):
    """ensure user with permission can change organization

    Args:
        user (_type_): _description_
    """
    pass


@pytest.mark.skip(reason="to be written")
def test_organizations_permission_delete_denied(user):
    """ensure non-admin user cant delete organization

    Args:
        user (_type_): _description_
    """
    pass


@pytest.mark.skip(reason="to be written")
def test_team_permission_add_in_org(user):
    """ensure user with add permission to an organization can add team

    Args:
        user (_type_): _description_
    """
    pass


@pytest.mark.skip(reason="to be written")
def test_team_permission_add_not_in_org(user):
    """ensure user with add permission to an organization can add team

    Args:
        user (_type_): _description_
    """
    pass


@pytest.mark.skip(reason="to be written")
def test_team_permission_change(user):
    """ensure user can change a team

    Args:
        user (_type_): _description_
    """
    pass


@pytest.mark.skip(reason="to be written")
def test_team_permission_delete(user):
    """ensure user can delete a team

    Args:
        user (_type_): _description_
    """
    pass


