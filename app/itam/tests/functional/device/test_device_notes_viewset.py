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

        self.item = Notes.objects.create(
            organization = self.organization,
            note = 'a note',
            usercreated = self.view_user,
            device = self.note_item
        )


        self.url_kwargs = {'device_id': self.note_item.id}

        self.url_view_kwargs = {'device_id': self.note_item.id, 'pk': self.item.pk }

        self.add_data = {'note': 'a note added', 'organization': self.organization.id}
