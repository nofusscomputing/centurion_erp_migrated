import pytest
import unittest

from access.models import TenancyObject
from access.tests.abstract.tenancy_object import TenancyObject as TenancyObjectTestCases

from app.tests.abstract.views import AddView, ChangeView, DeleteView, DisplayView, IndexView

from core.mixin.history_save import SaveHistory
from core.tests.abstract.models import Models



class BaseModel:
    """ Test cases for all models """

    model = None
    """ Model to test """


    @pytest.mark.skip(reason="figure out how to test sub-sub-class")
    def test_class_inherits_save_history(self):
        """ Confirm class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(self.model, TenancyObject)



class TenancyModel(
    BaseModel,
    TenancyObjectTestCases,
    Models
):
    """ Test cases for tenancy models"""

    model = None
    """ Model to test """



class ModelAdd(
    AddView
):
    """ Unit Tests for Model Add """



class ModelChange(
    ChangeView
):
    """ Unit Tests for Model Change """



class ModelDelete(
    DeleteView
):
    """ Unit Tests for Model delete """



class ModelDisplay(
    DisplayView
):
    """ Unit Tests for Model display """



class ModelIndex(
    IndexView
):
    """ Unit Tests for Model index """



class ModelCommon(
    ModelAdd,
    ModelChange,
    ModelDelete,
    ModelDisplay
):
    """ Unit Tests for all models """



class PrimaryModel(
    ModelCommon,
    ModelIndex
):
    """ Tests for Primary Models
    
    A Primary model is a model that is deemed a model that has the following views:
    - Add
    - Change
    - Delete
    - Display
    - Index
    """
