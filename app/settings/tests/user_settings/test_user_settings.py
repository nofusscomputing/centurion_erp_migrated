
from django.test import TestCase, Client

import pytest
import unittest
import requests



@pytest.mark.skip(reason="to be written")
def test_user_settings_on_create_of_user_settings_add():
    """ On Creation of a user their settings are created """
    pass


@pytest.mark.skip(reason="to be written")
def test_user_settings_on_delete_of_user_settings_removed():
    """ On Delete of a user their settings are removed """
    pass


@pytest.mark.skip(reason="to be written")
def test_user_settings_on_delete_organization_default_organization():
    """ On Delete of an organization, users default organization set to null """
    pass


@pytest.mark.skip(reason="to be written")
def test_user_settings_on_delete_organization_user_settings_not_deleted():
    """ On Delete of an organization, users settings are not deleted """
    pass


@pytest.mark.skip(reason="to be written")
def test_user_settings_only_owner_can_view():
    """ Only owner can access their settings url """
    pass


@pytest.mark.skip(reason="to be written")
def test_user_settings_only_owner_can_edit():
    """ Only owner and super admin can change user settings """
    pass


@pytest.mark.skip(reason="to be written")
def test_user_settings_super_admin_can_edit():
    """ Super admin can change user settings """
    pass

