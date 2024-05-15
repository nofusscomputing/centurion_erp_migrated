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


######################################################################
# SoF for loop for tests
#    for test in ['organization','team', 'users']
#
# permissions for each item as per the action plus view of the parent item
######################################################################
@pytest.mark.skip(reason="to be written")
def test_authorization_organization_view(user):
    """User of organization can view

        user requires permissions organization view
    """
    pass


@pytest.mark.skip(reason="to be written")
def test_authorization_organization_no_view(user):
    """User not part of organization cant view

        user requires permissions organization view
    """
    pass


###################################################################

@pytest.mark.skip(reason="to be written")
def test_authorization_team_permission_view(user):
    """ Ensure team can be viewed when user has correct permissions
    
        user requires permissions organization view and team view
    """
    pass

@pytest.mark.skip(reason="to be written")
def test_authorization_team_permission_no_view(user):
    """ Ensure team can't be viewed when user is missing permissions

        user requires permissions organization view and team view
    """
    pass



@pytest.mark.skip(reason="to be written")
def test_authorization_team_permission_add(user):
    """Ensure team can be added when user has correct permissions

        user requires permissions organization view and team add
    """
    pass

@pytest.mark.skip(reason="to be written")
def test_authorization_team_permission_no_view(user):
    """Ensure team can't be added when user is missing permissions

        user requires permissions organization view and team add
    """
    pass


@pytest.mark.skip(reason="to be written")
def test_authorization_team_permission_change(user):
    """Ensure team can be changed when user has correct permissions

        user requires permissions organization view and team change
    """
    pass

@pytest.mark.skip(reason="to be written")
def test_authorization_team_permission_no_change(user):
    """Ensure team can't be change when user is missing permissions

        user requires permissions organization view and team change
    """
    pass



@pytest.mark.skip(reason="to be written")
def test_authorization_team_permission_delete(user):
    """Ensure team can be deleted when user has correct permissions

        user requires permissions organization view and team delete
    """
    pass

@pytest.mark.skip(reason="to be written")
def test_authorization_team_permission_no_delete(user):
    """Ensure team can't be deleted when user is missing permissions

        user requires permissions organization view and team delete
    """
    pass




###################################################################



@pytest.mark.skip(reason="to be written")
def test_authorization_user_permission_add(user):
    """Ensure user can be added when user has correct permissions

        user requires permissions team view and user add
    """
    pass

@pytest.mark.skip(reason="to be written")
def test_authorization_user_permission_no_add(user):
    """Ensure user can't be added when user is missing permissions

        user requires permissions team view and user add
    """
    pass

@pytest.mark.skip(reason="to be written")
def test_authorization_user_permission_add_team_manager(user):
    """Ensure user can be added when user is team manager

        user requires permissions team view and user add
    """
    pass



@pytest.mark.skip(reason="to be written")
def test_authorization_user_permission_change(user):
    """Ensure user can be changed when user has correct permissions

        user requires permissions team view and user change
    """
    pass

@pytest.mark.skip(reason="to be written")
def test_authorization_user_permission_no_change(user):
    """Ensure user can't be change when user is missing permissions

        user requires permissions team view and user change
    """
    pass



@pytest.mark.skip(reason="to be written")
def test_authorization_user_permission_delete(user):
    """Ensure user can be deleted when user has correct permissions

        user requires permissions team view and user delete
    """
    pass

@pytest.mark.skip(reason="to be written")
def test_authorization_user_permission_no_delete(user):
    """Ensure user can't be deleted when user is missing permissions

        user requires permissions team view and user delete
    """
    pass

@pytest.mark.skip(reason="to be written")
def test_authorization_user_permission_delete_team_manager(user):
    """Ensure user can be deleted when user is team manager

        user requires permissions team view and user delete
    """
    pass

######################################################################
# EoF for loop for tests
#    for test in ['organization','team']
######################################################################

# is_superuser to be able to view, add, change, delete for all objects

