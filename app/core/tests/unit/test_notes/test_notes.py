import pytest
import unittest
import requests

from django.test import TestCase

from access.models import Organization

from app.tests.abstract.models import TenancyModel

from core.models.notes import Notes

from itam.models.device import Device


class NotesModel(
    TestCase,
    TenancyModel
):

    model = Notes


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a device
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization


        self.item = self.model.objects.create(
            organization=organization,
            note = 'note',
            device = Device.objects.create(
                organization=organization,
                name = 'note device',
            ),
        )


    @pytest.mark.skip(reason="to be written")
    def test_note_new_correct_usercreated():
        """ The user who added the note must be added to the note """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_note_new_correct_usermodified():
        """ The user who edited the note must be added to the note """
        pass


