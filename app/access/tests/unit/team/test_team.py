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