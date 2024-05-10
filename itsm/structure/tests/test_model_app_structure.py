from django.test import TestCase

import pytest
import requests
import unittest

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from structure.models import Organization, Team


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

    assert 'Ensure this value has at most 200 characters' in str(e.value)


@pytest.mark.django_db
def test_team_name_character_count(team) -> None:
    team.name = 'A' * 256

    with pytest.raises(ValidationError) as e:
        team.full_clean()

    assert 'Ensure this value has at most 200 characters' in str(e.value)
