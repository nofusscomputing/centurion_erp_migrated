import pytest
import unittest

from app.tests.abstract.views import AddView, ChangeView, DeleteView, DisplayView, IndexView



class BaseModel:
    """ Test cases for all models """

    model = None
    """ Model to test """




class TenancyModel(
    BaseModel,
    TenancyObjectTestCases
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
