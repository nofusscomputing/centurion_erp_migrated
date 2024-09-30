
from django.test import TestCase



class ModelAttributesUnit:
    """ Unit Tests For model attributes.

    These tests ensure that models contian the required attributes that are
    used by serializers to update the HTTP/Options method data.
    """

    model = None
    """Model to Test"""


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

