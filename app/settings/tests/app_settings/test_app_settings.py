
from django.test import TestCase, Client

import pytest
import unittest
import requests



@pytest.mark.skip(reason="to be written")
def test_app_settings_only_super_admin_can_access():
    """ Only super admin can access app settings """
    pass


@pytest.mark.skip(reason="to be written")
def test_app_settings_software_is_global_organization_must_be_set():
    """ If field software_is_global=true an organization must be set """
    pass


@pytest.mark.skip(reason="to be written")
def test_app_settings_software_is_global_create_software():
    """ If field software_is_global=true on software creation regardless of user settings
    software is created in global organization with global=true
    """
    pass

