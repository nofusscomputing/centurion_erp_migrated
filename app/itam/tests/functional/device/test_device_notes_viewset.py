import pytest

from django.test import TestCase

from core.tests.abstract.test_notes_viewset import NoteViewSetCommon

from core.models.notes import Notes

from itam.models.device import Device



class DeviceNotePermissionsAPI(
    NoteViewSetCommon,
    TestCase,
):

    app_namespace = 'API'
    
    url_name = '_api_v2_device_notes'


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a team
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        super().setUpTestData()



        self.note_item = Device.objects.create(
            organization = self.organization,
            name = 'history-device'
        )

        self.note_item_b = Device.objects.create(
            organization = self.different_organization,
            name = 'history-device-b'
        )

        self.item = Notes.objects.create(
            organization = self.organization,
            note = 'a note',
            usercreated = self.view_user,
            device = self.note_item
        )

        self.other_org_item = Notes.objects.create(
            organization = self.different_organization,
            note = 'b note',
            usercreated = self.view_user,
            device = self.note_item_b
        )


        self.url_kwargs = {'device_id': self.note_item.id}

        self.url_view_kwargs = {'device_id': self.note_item.id, 'pk': self.item.pk }

        self.add_data = {'note': 'a note added', 'organization': self.organization.id}


    def test_returned_data_from_user_and_global_organizations_only(self):
        """Check items returned

        This test case is a over-ride of a test case with the same name.
        This model is not a tenancy model making this test not-applicable.

        Items returned from the query Must be from the users organization and
        global ONLY!
        """
        pass