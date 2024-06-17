import pytest
import unittest

from django.test import TestCase, Client


from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_permissions import APIPermissions


@pytest.mark.skip(reason="to be written")
class TeamUsersPermissionsAPI(TestCase, APIPermissions):

    model = TeamUsers
