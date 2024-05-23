
from django.test import TestCase, Client

import pytest
import unittest
import requests




@pytest.mark.skip(reason="to be written")
def test_note_new_correct_operating_system():
    """ On creation of operating system note the operating system must be added """
    pass



@pytest.mark.skip(reason="to be written")
def test_note_auth_view_operating_system():
    """ Ensure that if the user doesn't have view permissions for notes, they can't see any notes
    
    user must also have view permissions for the opject the note is for
    """
    pass


@pytest.mark.skip(reason="to be written")
def test_note_auth_add_operating_system():
    """ Ensure that if the user doesn't have add permissions for notes, they can't add any notes
    
    user must also have view permissions for the opject the note is for
    """
    pass


@pytest.mark.skip(reason="to be written")
def test_note_auth_edit_operating_system():
    """ Ensure that if the user doesn't have edit permissions for notes, they can't edit any notes
    
    user must also have view permissions for the opject the note is for
    """
    pass


@pytest.mark.skip(reason="to be written")
def test_note_auth_delete_operating_system():
    """ Ensure that if the user doesn't have delete permissions for notes, they can't delete any notes
    
    user must also have view permissions for the opject the note is for
    """
    pass
