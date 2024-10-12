import importlib
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


    def test_field_exists_verbose_name_plural(self):
        """Test for existance of field in `<model>.Meta`

        Field is required for `templates/detail.html.js`

        Attribute `verbose_name_plural` must be defined in `Meta` class.
        """

        assert 'verbose_name_plural' in self.model._meta.original_attrs


    def test_field_not_empty_verbose_name_plural(self):
        """Test field `<model>.Meta` is not empty

        Field is required for `templates/detail.html.js`

        Attribute `verbose_name_plural` must be defined in `Meta` class.
        """

        assert self.model._meta.original_attrs['verbose_name_plural'] is not None


    def test_field_type_verbose_name_plural(self):
        """Test field `<model>.Meta` is not empty

        Field is required for `templates/detail.html.js`

        Attribute `verbose_name_plural` must be of type str.
        """

        assert type(self.model._meta.original_attrs['verbose_name_plural']) is str


    def test_field_exists_verbose_name(self):
        """Test for existance of field in `<model>.Meta`

        Field is required for `templates/detail.html.js`

        Attribute `verbose_name` must be defined in `Meta` class.
        """

        assert 'verbose_name' in self.model._meta.original_attrs


    def test_field_not_empty_verbose_name(self):
        """Test field `<model>.Meta` is not empty

        Field is required for `templates/detail.html.js`

        Attribute `verbose_name` must be defined in `Meta` class.
        """

        assert self.model._meta.original_attrs['verbose_name'] is not None


    def test_field_type_verbose_name(self):
        """Test field `<model>.Meta` is not empty

        Field is required for `templates/detail.html.js`

        Attribute `verbose_name` must be of type str.
        """

        assert type(self.model._meta.original_attrs['verbose_name']) is str



    def test_attribute_exists_table_fields(self):
        """Attrribute Test, Exists

        Ensure attribute `table_fields` exists
        """

        assert hasattr(self.model, 'table_fields')


    def test_attribute_type_table_fields(self):
        """Attrribute Test, Type

        Ensure attribute `table_fields` is of type `list`
        """

        assert type(self.model.table_fields) is list


    def test_attribute_not_callable_table_fields(self):
        """Attrribute Test, Not Callable

        Attribute must be a property

        Ensure attribute `table_fields` is not callable.
        """

        assert not callable(self.model.table_fields)



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
