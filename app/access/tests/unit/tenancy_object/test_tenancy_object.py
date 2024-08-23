import pytest
import unittest

from django.test import TestCase

from access.models import TenancyObject, TenancyManager

from core.mixin.history_save import SaveHistory

from unittest.mock import patch



class TenancyManagerTests(TestCase):

    item = TenancyManager


    def test_has_attribute_get_queryset(self):
        """ Field organization exists """
        
        assert hasattr(self.item, 'get_queryset')


    def test_is_function_get_queryset(self):
        """ Attribute 'get_organization' is a function """
        
        assert callable(self.item.get_queryset)



class TenancyObjectTests(TestCase):

    item = TenancyObject


    def test_class_inherits_save_history(self):
        """ Confirm class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(TenancyObject, SaveHistory)


    def test_has_attribute_organization(self):
        """ Field organization exists """
        
        assert hasattr(self.item, 'organization')


    def test_has_attribute_is_global(self):
        """ Field organization exists """
        
        assert hasattr(self.item, 'is_global')


    def test_has_attribute_model_notes(self):
        """ Field organization exists """
        
        assert hasattr(self.item, 'model_notes')


    def test_has_attribute_get_organization(self):
        """ Function 'get_organization' Exists """
        
        assert hasattr(self.item, 'get_organization')


    def test_is_function_get_organization(self):
        """ Attribute 'get_organization' is a function """
        
        assert callable(self.item.get_organization)


    @pytest.mark.skip(reason="figure out how to test abstract class")
    def test_has_attribute_objects(self):
        """ Attribute Check

        attribute `objects` must be set to `access.models.TenancyManager()`
        """

        assert 'objects' in self.item


    @pytest.mark.skip(reason="figure out how to test abstract class")
    def test_attribute_not_none_objects(self):
        """ Attribute Check

        attribute `objects` must be set to `access.models.TenancyManager()`
        """

        assert self.item.objects is not None
