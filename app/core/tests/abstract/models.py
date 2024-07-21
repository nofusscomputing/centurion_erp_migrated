import pytest
import unittest

from django.test import TestCase

from unittest.mock import patch

from access.models import TenancyManager


class Models:
    """ Test cases for Model Abstract Classes """


    
    def test_model_class_tenancy_manager_function_get_queryset(self):
        """ Function Check

        function `get_queryset()` must exist
        """

        assert hasattr(self.model.objects, 'get_queryset')

        assert callable(self.model.objects.get_queryset)


    @patch.object(TenancyManager, 'get_queryset')
    def test_model_class_tenancy_manager_function_get_queryset_called(self, get_queryset):
        """ Function Check

        function `access.models.TenancyManager.get_queryset()` within the Tenancy manager must
        be called as this function limits queries to the current users organizations.
        """

        self.model.objects.filter()

        assert get_queryset.called


    @pytest.mark.skip(reason="write test")
    def test_model_class_tenancy_manager_results_get_queryset(self):
        """ Function Results Check

        function `get_queryset()` must not return data from any organization the user is
        not part of.
        """

        pass


    @pytest.mark.skip(reason="write test")
    def test_model_class_tenancy_manager_results_get_queryset_super_user(self):
        """ Function Results Check

        function `get_queryset()` must return un-filtered data for super-user.
        """

        pass


