from django.test import TestCase

import pytest
import requests
import unittest

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from access.models import Organization, Team


@pytest.fixture
def organization() -> Organization:
    return Organization.objects.create(
        name='Test org',
    )


@pytest.fixture
def team() -> Team:
    return Team.objects.create(
        name='Team one',
        organization = Organization.objects.create(
            name='Test org',
        ),
    )


@pytest.mark.django_db
def test_org_name_character_count(organization) -> None:

    organization.name = 'A' * 256

    with pytest.raises(ValidationError) as e:
        organization.full_clean()

    assert 'Ensure this value has at most 50 characters' in str(e.value)


@pytest.mark.skip(reason="Already Tested by django devs as Team uses Group as base class")
def test_team_name_character_count(team) -> None:
    pass


@pytest.mark.skip(reason="to be written")
def test_team_cant_edit_org(user):
    """The org the team belongs to must not be editable

    Args:
        user (_type_): _description_
    """
    pass


@pytest.mark.skip(reason="to be written")
def test_team_create_updates_group_name(user):
    """On Creation of a Team, the team (group) name be set to <group name>_<team name>
    and contain no spaces and be lower case.

    Args:
        user (_type_): _description_
    """
    pass

@pytest.mark.skip(reason="to be written")
def test_team_edit_updates_group_name(user):
    """Every Edit to a Team must update the team (group) name to <group name>_<team name>
    and contain no spaces and be lower case.

    Args:
        user (_type_): _description_
    """
    pass

@pytest.mark.skip(reason="to be written")
def test_permission_organization_view(user):
    """View Permission required to view organization.

    Args:
        user (_type_): _description_
    """
    pass


# for tests:
#   test_permission_<model>_<permission>_returns_403
#   test_permission_<model>_<permission>_redirects_login
#
# All model and permission combinations to be tested

@pytest.mark.skip(reason="to be written")
def test_permission_organization_view_returns_403(user):
    """View Permission required to view organization.

    if it's missing and the user is logged on, a 403 must be returned for a logged in user.

    Args:
        user (_type_): _description_
    """
    pass


@pytest.mark.skip(reason="to be written")
def test_permission_organization_view_redirects_login(user):
    """View Permission required to view organization.

    if user not logged in they should be redirected to the login page.

    Args:
        user (_type_): _description_
    """
    pass
