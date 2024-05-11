from django.conf import settings
from django.shortcuts import reverse
from django.test import TestCase, Client

import pytest
import unittest

from access.models import Organization


@pytest.mark.django_db
def test_setting_login_required():
    """Some docstring defining what the test is checking."""
    client = Client()
    url = reverse('home')
    # client.force_login(user)
    # default_settings = settings
    settings.LOGIN_REQUIRED = True

    response = client.get(url)

    assert response.status_code == 302

    # settings = default_settings



@pytest.mark.django_db
def test_setting_login_required_not():
    """Some docstring defining what the test is checking."""
    client = Client()
    url = reverse('home')
    
    settings.LOGIN_REQUIRED = False

    response = client.get(url)

    assert response.status_code == 200
