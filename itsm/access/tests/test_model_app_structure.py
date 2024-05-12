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
def test_authorization_organization_view(user):
    """User of organization can view
    """
    pass


@pytest.mark.skip(reason="to be written")
def test_authorization_organization_no_view(user):
    """User not part of organization cant view
    """
    pass


@pytest.mark.skip(reason="to be written")
def test_authorization_organization_object_view(user):
    """User part of organization can view organization object
    """
    pass


@pytest.mark.skip(reason="to be written")
def test_authorization_organization_object_no_view(user):
    """User not part of organization cant view organization object
    """
    pass


@pytest.mark.skip(reason="to be written")
def test_authorization_organization_object_add(user):
    """User part of organization can view organization object
    """
    pass


@pytest.mark.skip(reason="to be written")
def test_authorization_organization_object_no_add(user):
    """User not part of organization cant view organization object
    """
    pass


@pytest.mark.skip(reason="to be written")
def test_authorization_organization_object_edit(user):
    """User part of organization can view organization object
    """
    pass


@pytest.mark.skip(reason="to be written")
def test_authorization_organization_object_no_edit(user):
    """User not part of organization cant view organization object
    """
    pass


@pytest.mark.skip(reason="to be written")
def test_authorization_organization_object_delete(user):
    """User part of organization can view organization object
    """
    pass


@pytest.mark.skip(reason="to be written")
def test_authorization_organization_object_no_delete(user):
    """User not part of organization cant view organization object
    """
    pass
