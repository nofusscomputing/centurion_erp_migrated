import inspect
import pytest
import unittest



class AddView:
    """ Testing of Display view """

    add_module: str = None
    """ Full module path to test """

    add_view: str = None
    """ View Class name to test """


    def test_view_add_attribute_not_exists_fields(self):
        """ Attribute does not exists test
        
        Ensure that `fields` attribute is not defined as the expectation is that a form will be used.
        """

        module = __import__(self.add_module, fromlist=[self.add_view])

        assert hasattr(module, self.add_view)

        viewclass = getattr(module, self.add_view)

        assert viewclass.fields is None


    def test_view_add_attribute_exists_form_class(self):
        """ Attribute exists test
        
        Ensure that `form_class` attribute is defined as it's required.
        """

        module = __import__(self.add_module, fromlist=[self.add_view])

        assert hasattr(module, self.add_view)

        viewclass = getattr(module, self.add_view)

        assert hasattr(viewclass, 'form_class')


    def test_view_add_attribute_type_form_class(self):
        """ Attribute Type Test
        
        Ensure that `form_class` attribute is a class.
        """

        module = __import__(self.add_module, fromlist=[self.add_view])

        assert hasattr(module, self.add_view)

        viewclass = getattr(module, self.add_view)

        assert inspect.isclass(viewclass.form_class)


    def test_view_add_attribute_exists_model(self):
        """ Attribute exists test
        
        Ensure that `model` attribute is defined as it's required .
        """

        module = __import__(self.add_module, fromlist=[self.add_view])

        assert hasattr(module, self.add_view)

        viewclass = getattr(module, self.add_view)

        assert hasattr(viewclass, 'model')


    def test_view_add_attribute_exists_permission_required(self):
        """ Attribute exists test
        
        Ensure that `permission_required` attribute is defined as it's required.
        """

        module = __import__(self.add_module, fromlist=[self.add_view])

        assert hasattr(module, self.add_view)

        viewclass = getattr(module, self.add_view)

        assert hasattr(viewclass, 'permission_required')


    def test_view_add_attribute_type_permission_required(self):
        """ Attribute Type Test
        
        Ensure that `permission_required` attribute is a list
        """

        module = __import__(self.add_module, fromlist=[self.add_view])

        assert hasattr(module, self.add_view)

        viewclass = getattr(module, self.add_view)

        assert type(viewclass.permission_required) is list


    def test_view_add_attribute_exists_template_name(self):
        """ Attribute exists test
        
        Ensure that `template_name` attribute is defined as it's required.
        """

        module = __import__(self.add_module, fromlist=[self.add_view])

        assert hasattr(module, self.add_view)

        viewclass = getattr(module, self.add_view)

        assert hasattr(viewclass, 'template_name')


    def test_view_add_attribute_type_template_name(self):
        """ Attribute Type Test
        
        Ensure that `template_name` attribute is a string.
        """

        module = __import__(self.add_module, fromlist=[self.add_view])

        assert hasattr(module, self.add_view)

        viewclass = getattr(module, self.add_view)

        assert type(viewclass.template_name) is str



class ChangeView:
    """ Testing of Display view """

    change_module: str = None
    """ Full module path to test """

    change_view: str = None
    """ Change Class name to test """


    def test_view_change_attribute_not_exists_fields(self):
        """ Attribute does not exists test
        
        Ensure that `fields` attribute is not defined as the expectation is that a form will be used.
        """

        module = __import__(self.change_module, fromlist=[self.change_view])

        assert hasattr(module, self.change_view)

        viewclass = getattr(module, self.change_view)

        assert viewclass.fields is None


    def test_view_change_attribute_exists_form_class(self):
        """ Attribute exists test
        
        Ensure that `form_class` attribute is defined as it's required.
        """

        module = __import__(self.change_module, fromlist=[self.change_view])

        assert hasattr(module, self.change_view)

        viewclass = getattr(module, self.change_view)

        assert hasattr(viewclass, 'form_class')


    def test_view_change_attribute_type_form_class(self):
        """ Attribute Type Test
        
        Ensure that `form_class` attribute is a string.
        """

        module = __import__(self.change_module, fromlist=[self.change_view])

        assert hasattr(module, self.change_view)

        viewclass = getattr(module, self.change_view)

        assert inspect.isclass(viewclass.form_class)


    def test_view_change_attribute_exists_model(self):
        """ Attribute exists test
        
        Ensure that `model` attribute is defined as it's required .
        """

        module = __import__(self.change_module, fromlist=[self.change_view])

        assert hasattr(module, self.change_view)

        viewclass = getattr(module, self.change_view)

        assert hasattr(viewclass, 'model')


    def test_view_change_attribute_exists_permission_required(self):
        """ Attribute exists test
        
        Ensure that `permission_required` attribute is defined as it's required.
        """

        module = __import__(self.change_module, fromlist=[self.change_view])

        assert hasattr(module, self.change_view)

        viewclass = getattr(module, self.change_view)

        assert hasattr(viewclass, 'permission_required')


    def test_view_change_attribute_type_permission_required(self):
        """ Attribute Type Test
        
        Ensure that `permission_required` attribute is a list
        """

        module = __import__(self.change_module, fromlist=[self.change_view])

        assert hasattr(module, self.change_view)

        viewclass = getattr(module, self.change_view)

        assert type(viewclass.permission_required) is list


    def test_view_change_attribute_exists_template_name(self):
        """ Attribute exists test
        
        Ensure that `template_name` attribute is defined as it's required.
        """

        module = __import__(self.change_module, fromlist=[self.change_view])

        assert hasattr(module, self.change_view)

        viewclass = getattr(module, self.change_view)

        assert hasattr(viewclass, 'template_name')


    def test_view_change_attribute_type_template_name(self):
        """ Attribute Type Test
        
        Ensure that `template_name` attribute is a string.
        """

        module = __import__(self.change_module, fromlist=[self.change_view])

        assert hasattr(module, self.change_view)

        viewclass = getattr(module, self.change_view)

        assert type(viewclass.template_name) is str



class DeleteView:
    """ Testing of Display view """

    delete_module: str = None
    """ Full module path to test """

    delete_view: str = None
    """ Delete Class name to test """


    def test_view_delete_attribute_exists_model(self):
        """ Attribute exists test
        
        Ensure that `model` attribute is defined as it's required .
        """

        module = __import__(self.delete_module, fromlist=[self.delete_view])

        assert hasattr(module, self.delete_view)

        viewclass = getattr(module, self.delete_view)

        assert hasattr(viewclass, 'model')


    def test_view_delete_attribute_exists_permission_required(self):
        """ Attribute exists test
        
        Ensure that `model` attribute is defined as it's required .
        """

        module = __import__(self.delete_module, fromlist=[self.delete_view])

        assert hasattr(module, self.delete_view)

        viewclass = getattr(module, self.delete_view)

        assert hasattr(viewclass, 'permission_required')


    def test_view_delete_attribute_type_permission_required(self):
        """ Attribute Type Test
        
        Ensure that `permission_required` attribute is a list
        """

        module = __import__(self.delete_module, fromlist=[self.delete_view])

        assert hasattr(module, self.delete_view)

        viewclass = getattr(module, self.delete_view)

        assert type(viewclass.permission_required) is list


    def test_view_delete_attribute_exists_template_name(self):
        """ Attribute exists test
        
        Ensure that `template_name` attribute is defined as it's required.
        """

        module = __import__(self.delete_module, fromlist=[self.delete_view])

        assert hasattr(module, self.delete_view)

        viewclass = getattr(module, self.delete_view)

        assert hasattr(viewclass, 'template_name')


    def test_view_delete_attribute_type_template_name(self):
        """ Attribute Type Test
        
        Ensure that `template_name` attribute is a string.
        """

        module = __import__(self.delete_module, fromlist=[self.delete_view])

        assert hasattr(module, self.delete_view)

        viewclass = getattr(module, self.delete_view)

        assert type(viewclass.template_name) is str



class DisplayView:
    """ Testing of Display view """

    display_module: str = None
    """ Full module path to test """

    display_view: str = None
    """ Change Class name to test """


    def test_view_display_attribute_exists_model(self):
        """ Attribute exists test
        
        Ensure that `model` attribute is defined as it's required .
        """

        module = __import__(self.display_module, fromlist=[self.display_view])

        assert hasattr(module, self.display_view)

        viewclass = getattr(module, self.display_view)

        assert hasattr(viewclass, 'model')


    def test_view_display_attribute_exists_permission_required(self):
        """ Attribute exists test
        
        Ensure that `permission_required` attribute is defined as it's required.
        """

        module = __import__(self.display_module, fromlist=[self.display_view])

        assert hasattr(module, self.display_view)

        viewclass = getattr(module, self.display_view)

        assert hasattr(viewclass, 'permission_required')


    def test_view_display_attribute_type_permission_required(self):
        """ Attribute Type Test
        
        Ensure that `permission_required` attribute is a list
        """

        module = __import__(self.display_module, fromlist=[self.display_view])

        assert hasattr(module, self.display_view)

        viewclass = getattr(module, self.display_view)

        assert type(viewclass.permission_required) is list


    def test_view_display_attribute_exists_template_name(self):
        """ Attribute exists test
        
        Ensure that `template_name` attribute is defined as it's required.
        """

        module = __import__(self.display_module, fromlist=[self.display_view])

        assert hasattr(module, self.display_view)

        viewclass = getattr(module, self.display_view)

        assert hasattr(viewclass, 'template_name')


    def test_view_display_attribute_type_template_name(self):
        """ Attribute Type Test
        
        Ensure that `template_name` attribute is a string.
        """

        module = __import__(self.display_module, fromlist=[self.display_view])

        assert hasattr(module, self.display_view)

        viewclass = getattr(module, self.display_view)

        assert type(viewclass.template_name) is str



class IndexView:
    """ Testing of Display view """

    index_module: str = None
    """ Full module path to test """

    index_view: str = None
    """ Index Class name to test """


    def test_view_index_attribute_exists_model(self):
        """ Attribute exists test
        
        Ensure that `model` attribute is defined as it's required .
        """

        module = __import__(self.index_module, fromlist=[self.index_view])

        assert hasattr(module, self.index_view)

        viewclass = getattr(module, self.index_view)

        assert hasattr(viewclass, 'model')


    def test_view_index_attribute_exists_permission_required(self):
        """ Attribute exists test
        
        Ensure that `model` attribute is defined as it's required .
        """

        module = __import__(self.index_module, fromlist=[self.index_view])

        assert hasattr(module, self.index_view)

        viewclass = getattr(module, self.index_view)

        assert hasattr(viewclass, 'permission_required')


    def test_view_index_attribute_type_permission_required(self):
        """ Attribute Type Test
        
        Ensure that `permission_required` attribute is a list
        """

        module = __import__(self.index_module, fromlist=[self.index_view])

        assert hasattr(module, self.index_view)

        viewclass = getattr(module, self.index_view)

        assert type(viewclass.permission_required) is list


    def test_view_index_attribute_exists_template_name(self):
        """ Attribute exists test
        
        Ensure that `template_name` attribute is defined as it's required.
        """

        module = __import__(self.index_module, fromlist=[self.index_view])

        assert hasattr(module, self.index_view)

        viewclass = getattr(module, self.index_view)

        assert hasattr(viewclass, 'template_name')


    def test_view_index_attribute_type_template_name(self):
        """ Attribute Type Test
        
        Ensure that `template_name` attribute is a string.
        """

        module = __import__(self.index_module, fromlist=[self.index_view])

        assert hasattr(module, self.index_view)

        viewclass = getattr(module, self.index_view)

        assert type(viewclass.template_name) is str



class AllViews(
    AddView,
    ChangeView,
    DeleteView,
    DisplayView,
    IndexView
):
    """ Abstract test class containing ALL view tests """

    add_module: str = None
    """ Full module path to test """

    add_view: str = None
    """ View Class name to test """

    change_module: str = None
    """ Full module path to test """

    change_view: str = None
    """ Change Class name to test """

    delete_module: str = None
    """ Full module path to test """

    delete_view: str = None
    """ Delete Class name to test """

    display_module: str = None
    """ Full module path to test """

    display_view: str = None
    """ Change Class name to test """

    index_module: str = None
    """ Full module path to test """

    index_view: str = None
    """ Index Class name to test """

