import pytest
import unittest

from django.test import TestCase



class Models:
    """ Test cases for Model Abstract Classes """



    @pytest.mark.skip(reason="write test")
    def test_model_class_tenancy_manager_function_get_queryset(self):
        """ Function Check

        function `get_queryset()` must exist
        """

        pass


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


    @pytest.mark.skip(reason="write test")
    def test_model_class_tenancy_object_attribute_objects(self):
        """ Attribute Check

        attribute `objects` must be set to `access.models.TenancyManager()`
        """

        pass


    @pytest.mark.skip(reason="write test")
    def test_model_class_inheritence_tenancy_object_save_history(self):
        """ Class inheritence Check

        Class inherits from `core.mixin.history_save.SaveHistory`
        """

        pass

