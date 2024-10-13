import pytest
import unittest

from django.test import TestCase, Client

from access.models import Organization, Team, TeamUsers, Permission

from app.tests.abstract.models import TenancyModel



class TeamModel(
    TestCase,
    TenancyModel
):

    model = Team



    @classmethod
    def setUpTestData(self):
        """ Setup Test

        """

        self.parent_item = Organization.objects.create(name='test_org')

        different_organization = Organization.objects.create(name='test_different_organization')

        self.item = self.model.objects.create(
            organization=self.parent_item,
            name = 'teamone'
        )


    def test_model_has_property_parent_object(self):
        """ Check if model contains 'parent_object'
        
            This is a required property for all models that have a parent
        """

        assert hasattr(self.model, 'parent_object')


    def test_model_property_parent_object_returns_object(self):
        """ Check if model contains 'parent_object'
        
            This is a required property for all models that have a parent
        """

        assert self.item.parent_object is self.parent_item


    @pytest.mark.skip(reason="to be written")
    def test_function_save_attributes():
        """ Ensure save Attributes function match django default

        the save method is overridden. the function attributes must match default django method
        """
        pass


    @pytest.mark.skip(reason="uses Django group manager")
    def test_attribute_is_type_objects(self):
        pass

    @pytest.mark.skip(reason="uses Django group manager")
    def test_model_class_tenancy_manager_function_get_queryset_called(self):
        pass


    def test_model_fields_parameter_not_empty_help_text(self):
        """Test Field called with Parameter

        This is a custom test of a test derived of the samae name. It's required
        as the team model extends the Group model.

        During field creation, paramater `help_text` must not be `None` or empty ('')
        """

        group_mode_fields_to_ignore: list = [
            'id',
            'name',
            'group_ptr_id'
        ]

        fields_have_test_value: bool = True

        for field in self.model._meta.fields:

            if field.attname in group_mode_fields_to_ignore:

                continue

            print(f'Checking field {field.attname} is not empty')

            if (
                field.help_text is None
                or field.help_text == ''
            ):

                print(f'    Failure on field {field.attname}')

                fields_have_test_value = False


        assert fields_have_test_value

    def test_model_fields_parameter_type_verbose_name(self):
        """Test Field called with Parameter

        This is a custom test of a test derived of the samae name. It's required
        as the team model extends the Group model.

        During field creation, paramater `verbose_name` must be of type str
        """

        group_mode_fields_to_ignore: list = [
            'name',
        ]

        fields_have_test_value: bool = True

        for field in self.model._meta.fields:

            if field.attname in group_mode_fields_to_ignore:

                continue

            print(f'Checking field {field.attname} is of type str')

            if not type(field.verbose_name) is str:

                print(f'    Failure on field {field.attname}')

                fields_have_test_value = False


        assert fields_have_test_value
