import pytest
import unittest

from django.test import TestCase

from access.models import TenancyObject

from unittest.mock import patch



class TenancyObject(TestCase):

    item = TenancyObject



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
