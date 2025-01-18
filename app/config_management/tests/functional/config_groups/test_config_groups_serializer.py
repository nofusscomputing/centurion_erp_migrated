import pytest

from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models import Organization

from app.tests.abstract.mock_view import MockView, User

from config_management.serializers.config_group import ConfigGroups, ConfigGroupModelSerializer



class ConfigGroupsValidationAPI(
    TestCase,
):

    model = ConfigGroups

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

        self.item_no_parent = self.model.objects.create(
            organization=organization,
            name = 'random title',
            config = { 'config_key': 'a value' }
        )

        self.item_has_parent = self.model.objects.create(
            organization=organization,
            name = 'random title two',
            parent = self.item_no_parent
        )



    def test_serializer_validation_no_name(self):
        """Serializer Validation Check

        Ensure that if creating and no name is provided a validation error occurs
        """

        with pytest.raises(ValidationError) as err:

            serializer = ConfigGroupModelSerializer(
                context = {
                    'request': self.mock_view.request,
                    'view': self.mock_view,
                },
                data={
                "organization": self.organization.id,
            })

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['name'][0] == 'required'



    def test_serializer_validation_update_existing_parnet_not_self(self):
        """Serializer Validation Check

        Ensure that if an existing item is assigned itself as it's parent group
        it raises a validation error
        """

        with pytest.raises(ValidationError) as err:

            serializer = ConfigGroupModelSerializer(
                self.item_has_parent,
                context = {
                    'request': self.mock_view.request,
                    'view': self.mock_view,
                },
                data={
                    "parent": self.item_has_parent.id
                },
                partial=True,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['parent'][0] == 'self_not_parent'


    def test_serializer_validation_update_existing_invalid_config_key(self):
        """Serializer Validation Check

        Ensure that if an existing item has it's config updated with an invalid config key
        a validation exception is raised.
        """

        invalid_config = self.item_no_parent.config.copy()
        invalid_config.update({ 'software': 'is invalid' })

        with pytest.raises(ValidationError) as err:

            serializer = ConfigGroupModelSerializer(
                self.item_no_parent,
                context = {
                    'request': self.mock_view.request,
                    'view': self.mock_view,
                },
                data={
                    "config": invalid_config
                },
                partial=True,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['config'][0] == 'invalid'
