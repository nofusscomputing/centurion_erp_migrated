import pytest
import unittest
import requests

from django.test import TestCase

from app.tests.abstract.models import TenancyModel

from core.models.notes import Notes


class NotesModel(
    TestCase,
    TenancyModel
):

    model = Notes


    @pytest.mark.skip(reason="to be written")
    def test_note_new_correct_usercreated():
        """ The user who added the note must be added to the note """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_note_new_correct_usermodified():
        """ The user who edited the note must be added to the note """
        pass


