import pytest

from django.test import TestCase

from core.tests.abstract.test_notes_viewset import NoteViewSetCommon

from core.models.notes import Notes

from itim.models.services import Service



class ServiceNotePermissionsAPI(
    NoteViewSetCommon,
    TestCase,
):

    app_namespace = 'API'
    
    url_name = '_api_v2_service_notes'


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



        self.note_item = Service.objects.create(
            organization = self.organization,
            name = 'history-device'
        )

        self.item = Notes.objects.create(
            organization = self.organization,
            note = 'a note',
            usercreated = self.view_user,
            service = self.note_item
        )

        self.other_org_item = Notes.objects.create(
            organization = self.different_organization,
            note = 'b note',
            usercreated = self.view_user,
            service = self.note_item
        )


        self.url_kwargs = {'service_id': self.note_item.id}

        self.url_view_kwargs = {'service_id': self.note_item.id, 'pk': self.item.pk }

        self.add_data = {'note': 'a note added', 'organization': self.organization.id}
