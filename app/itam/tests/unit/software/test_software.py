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


@pytest.mark.skip(reason="to be written")
def test_software_must_have_organization(user):
    """ Software must have organization set """
    pass

@pytest.mark.skip(reason="to be written")
def test_software_update_is_global_no_change(user):
    """Once software is set to global it can't be changed.

        global status can't be changed as non-global items may reference the item.
    """

    pass

@pytest.mark.skip(reason="to be written")
def test_software_prevent_delete_if_used(user):
    """Any software in use by a software must not be deleted.

        i.e. A software has an action set for the software.
    """

    pass
