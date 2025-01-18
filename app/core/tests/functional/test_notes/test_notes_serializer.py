import pytest

from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models import Organization

from core.serializers.notes import Notes, NoteModelSerializer

from app.tests.abstract.mock_view import MockView

from itam.models.device import Device



class NotesValidationAPI(
    TestCase,
):

    # model = ConfigGroups

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        2. Create an item
        """

        organization = Organization.objects.create(name='test_org')

        self.user = User.objects.create_user(username="test_user_view", password="password")

        self.mock_view = MockView( user = self.user )

        self.organization = organization

        self.device = Device.objects.create(
            organization = self.organization,
            name = 'notes-test'
        )

        # self.item_no_parent = self.model.objects.create(
        #     organization=organization,
        #     name = 'random title',
        #     config = { 'config_key': 'a value' }
        # )

        # self.item_has_parent = self.model.objects.create(
        #     organization=organization,
        #     name = 'random title two',
        #     parent = self.item_no_parent
        # )



    def test_serializer_validation_no_note(self):
        """Serializer Validation Check

        Ensure that if creating and no name is provided a validation error occurs
        """

        with pytest.raises(ValidationError) as err:

            serializer = NoteModelSerializer(
                context = {
                    'request': self.mock_view.request,
                    'view': self.mock_view,
                },
                data={
                "organization": self.organization.id,
            })

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['note'][0] == 'required'
