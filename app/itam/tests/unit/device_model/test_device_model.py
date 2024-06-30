# from django.conf import settings
# from django.shortcuts import reverse
from django.test import TestCase, Client

import pytest
import unittest
import requests

# from django.contrib.auth import get_user_model
# from django.core.exceptions import ValidationError
# from access.models import Organization

# class Test_app_structure_auth(unittest.TestCase):
# User = get_user_model()



@pytest.mark.skip(reason="to be written")
def test_device_model_software_action(user):
    """Ensure only software that is from the same organization or is global can be added to the device
    """
    pass


@pytest.mark.skip(reason="to be written")
def test_device_model_must_have_organization(user):
    """ Device Model must have organization set """
    pass


@pytest.mark.skip(reason="to be written")
def test_device_model_not_global(user):
    """Devices are not global items.

        Ensure that a device can't be set to be global.
    """
    pass


@pytest.mark.skip(reason="to be written")
def test_device_model_operating_system_version_only_one(user):
    """model deviceoperatingsystem must only contain one value per device
    """
    pass
