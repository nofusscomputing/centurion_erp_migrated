import pytest
import unittest

from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase, Client

from core.models.notes import Notes

from itam.models.device import Device



class NotesPermissions:
    """Test cases for Notes permissions

    !!! danger
        These test cases assume that the method of adding notes is via the view page
        of the model in question. If this changes, these tests will need to be re-written 
        so that that the actual method of access is tested.
    """    


    item: object
    """Created Model

    Create a new item. 
    """

    model = Notes
    """ The history Model """

    namespace: str = ''
    """ URL namespace for the history view"""

    name_view: str = '_history'
    """ URL view name for history """

    no_permissions_user: User
    """A User with no permissions to access the item
    
    Create in `setUpTestData`
    """

    different_organization_user: User
    """A User with the correct permissions to access the item

    This user must be in a different organization than the item
    
    Create in `setUpTestData`
    """

    view_user: User
    """A User with the correct permissions to access the item

    This user must be in the same organization as the item
    
    Create in `setUpTestData`
    """



    @pytest.mark.skip(reason="write test")
    def test_notes_no_permission_view_denied(self):
        """ Check correct permission for notes view

        Attempt to view with user missing permission
        """

        # test notes context is empty (and/or HTTP/403 returned??)

        pass


    @pytest.mark.skip(reason="write test")
    def test_notes_has_permission_view_different_organizaiton_denied(self):
        """ Check correct permission for notes view

        Attempt to view with user from different organization
        """

        # test notes context is empty (and/or HTTP/403 returned??)
        pass



    @pytest.mark.skip(reason="write test")
    def test_notes_has_permission_view(self):
        """ Check correct permission for notes view

        Attempt to view as user with view permission
        """

        # test notes context contains the notes
        pass


    @pytest.mark.skip(reason="write test")
    def test_notes_has_permission_add(self):
        """ Check correct permission for note add 

        Attempt to add a note as user with no permission
        """

        pass


    @pytest.mark.skip(reason="write test")
    def test_notes_has_permission_change(self):
        """ Check correct permission for notes change

        Make change with user who has notes change permission
        """

        pass


    @pytest.mark.skip(reason="write test")
    def test_notes_has_permission_delete(self):
        """ Check correct permission for notes delete

        Delete with user who has notes delete permission
        """

        pass
