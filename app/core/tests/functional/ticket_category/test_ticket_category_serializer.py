import pytest

from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models import Organization

from app.tests.abstract.mock_view import MockView, User

from core.serializers.ticket_category import TicketCategory, TicketCategoryModelSerializer



class TicketCategoryValidationAPI(
    TestCase,
):

    model = TicketCategory

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

        self.item = self.model.objects.create(
            organization=organization,
            name = 'random title',
        )



    def test_serializer_validation_add_valid_item(self):
        """Serializer Validation Check

        Ensure that a valid item it does not raise a validation error
        """

        serializer = TicketCategoryModelSerializer(
            context = {
                'request': self.mock_view.request,
                'view': self.mock_view,
            },
            data={
                "organization": self.organization.id,
                "name": 'new category'
            }
        )

        assert serializer.is_valid(raise_exception = True)



    def test_serializer_validation_self_not_parent(self):
        """Serializer Validation Check

        Ensure that a validation error is raised if an attempt to add
        self as parent category.
        """

        with pytest.raises(ValidationError) as err:

            serializer = TicketCategoryModelSerializer(
                self.item,
                context = {
                    'request': self.mock_view.request,
                    'view': self.mock_view,
                },
                data={
                    "parent": self.item.id,
                },
                partial = True
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['parent'][0] == 'parent_not_self'



    def test_serializer_validation_no_name(self):
        """Serializer Validation Check

        Ensure that if creating and no name is provided a validation error occurs
        """

        with pytest.raises(ValidationError) as err:

            serializer = TicketCategoryModelSerializer(
                context = {
                    'request': self.mock_view.request,
                    'view': self.mock_view,
                },
                data={
                "organization": self.organization.id,
            })

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['name'][0] == 'required'



    def test_serializer_validation_add_existing_allowed(self):
        """Serializer Validation Check

        Ensure that if adding the same item it raises a validation error
        """

        serializer = TicketCategoryModelSerializer(
            context = {
                'request': self.mock_view.request,
                'view': self.mock_view,
            },
            data={
                "organization": self.organization.id,
                "name": self.item.name
            }
        )

        assert serializer.is_valid(raise_exception = True)
