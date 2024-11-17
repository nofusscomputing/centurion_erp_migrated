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


    def test_attribute_exists_ordering(self):
        """Test for existance of field in `<model>.Meta`

        Attribute `ordering` must be defined in `Meta` class.
        """

        assert 'ordering' in self.model._meta.original_attrs


    def test_attribute_not_empty_ordering(self):
        """Test field `<model>.Meta` is not empty

        Attribute `ordering` must contain values
        """

        assert (
            self.model._meta.original_attrs['ordering'] is not None
            and len(list(self.model._meta.original_attrs['ordering'])) > 0
        )


    def test_attribute_type_ordering(self):
        """Test field `<model>.Meta` is not empty

        Attribute `ordering` must be of type list.
        """

        assert type(self.model._meta.original_attrs['ordering']) is list



    def test_model_fields_parameter_has_help_text(self):
        """Test Field called with Parameter

        During field creation, it should have been called with paramater `help_text`
        """

        fields_have_test_value: bool = True

        for field in self.model._meta.fields:

            print(f'Checking field {field.attname} has attribute "help_text"')

            if not hasattr(field, 'help_text'):

                print(f'    Failure on field {field.attname}')

                fields_have_test_value = False


        assert fields_have_test_value


    def test_model_fields_parameter_type_help_text(self):
        """Test Field called with Parameter

        During field creation, paramater `help_text` must be of type str
        """

        fields_have_test_value: bool = True

        for field in self.model._meta.fields:

            print(f'Checking field {field.attname} is of type str')

            if not type(field.help_text) is str:

                print(f'    Failure on field {field.attname}')

                fields_have_test_value = False


        assert fields_have_test_value


    def test_model_fields_parameter_not_empty_help_text(self):
        """Test Field called with Parameter

        During field creation, paramater `help_text` must not be `None` or empty ('')
        """

        fields_have_test_value: bool = True

        for field in self.model._meta.fields:

            print(f'Checking field {field.attname} is not empty')

            if (
                field.help_text is None
                or field.help_text == ''
            ):

                print(f'    Failure on field {field.attname}')

                fields_have_test_value = False


        assert fields_have_test_value



    def test_model_fields_parameter_has_verbose_name(self):
        """Test Field called with Parameter

        During field creation, it should have been called with paramater `verbose_name`
        """

        fields_have_test_value: bool = True

        for field in self.model._meta.fields:

            print(f'Checking field {field.attname} has attribute "verbose_name"')

            if not hasattr(field, 'verbose_name'):

                print(f'    Failure on field {field.attname}')

                fields_have_test_value = False


        assert fields_have_test_value


    def test_model_fields_parameter_type_verbose_name(self):
        """Test Field called with Parameter

        During field creation, paramater `verbose_name` must be of type str
        """

        fields_have_test_value: bool = True

        for field in self.model._meta.fields:

            print(f'Checking field {field.attname} is of type str')

            if not type(field.verbose_name) is str:

                print(f'    Failure on field {field.attname}')

                fields_have_test_value = False


        assert fields_have_test_value


    def test_model_fields_parameter_not_empty_verbose_name(self):
        """Test Field called with Parameter

        During field creation, paramater `verbose_name` must not be `None` or empty ('')
        """

        fields_have_test_value: bool = True

        for field in self.model._meta.fields:

            print(f'Checking field {field.attname} is not empty')

            if (
                field.verbose_name is None
                or field.verbose_name == ''
            ):

                print(f'    Failure on field {field.attname}')

                fields_have_test_value = False


        assert fields_have_test_value





    def test_attribute_exists_get_url(self):
        """Test for existance of field in `<model>`

        Attribute `get_url` must be defined in class.
        """

        assert hasattr(self.item, 'get_url')


    def test_attribute_not_empty_get_url(self):
        """Test field `<model>` is not empty

        Attribute `get_url` must contain values
        """

        assert self.item.get_url() is not None


    def test_attribute_type_get_url(self):
        """Test field `<model>`type

        Attribute `get_url` must be str
        """

        assert type(self.item.get_url()) is str


    def test_attribute_callable_get_url(self):
        """Test field `<model>` callable

        Attribute `get_url` must be a function
        """

        assert callable(self.item.get_url)



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



    def test_attribute_exists_page_layout(self):
        """Attrribute Test, Exists

        Ensure attribute `page_layout` exists
        """

        assert hasattr(self.model, 'page_layout')


    def test_attribute_type_page_layout(self):
        """Attrribute Test, Type

        Ensure attribute `page_layout` is of type `list`
        """

        assert type(self.model.page_layout) is list


    def test_attribute_not_callable_page_layout(self):
        """Attrribute Test, Not Callable

        Attribute must be a property

        Ensure attribute `page_layout` is not callable.
        """

        assert not callable(self.model.page_layout)



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
