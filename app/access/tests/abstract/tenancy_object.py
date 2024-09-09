import pytest
import unittest

from access.models import TenancyManager



class TenancyObject:
    """ Tests for checking TenancyObject """

    model = None
    """ Model to be tested """

    should_model_history_be_saved: bool = True
    """ Should model history be saved.

    By default this should always be 'True', however in special
    circumstances, this may not be desired.
    """


    def test_history_save(self):
        """Confirm the desired intent for saving model history."""

        assert self.model.save_model_history == self.should_model_history_be_saved


    def test_has_attr_get_organization(self):
        """ TenancyObject attribute check

        TenancyObject has function get_organization
        """

        assert hasattr(self.model, 'get_organization')


    def test_has_attr_is_global(self):
        """ TenancyObject attribute check

        TenancyObject has field is_global
        """

        assert hasattr(self.model, 'is_global')



    def test_has_attr_model_notes(self):
        """ TenancyObject attribute check

        TenancyObject has field model_notes
        """

        assert hasattr(self.model, 'model_notes')



    def test_has_attr_organization(self):
        """ TenancyObject attribute check

        TenancyObject has field organization
        """

        assert hasattr(self.model, 'organization')



    @pytest.mark.skip(reason="to be written")
    def test_create_no_organization_fails(self):
        """ Devices must be assigned an organization

        Must not be able to create an item without an organization
        """
        pass



    @pytest.mark.skip(reason="to be written")
    def test_edit_no_organization_fails(self):
        """ Devices must be assigned an organization

        Must not be able to edit an item without an organization
        """
        pass


    def test_has_attr_organization(self):
        """ TenancyObject attribute check

        TenancyObject has function objects
        """

        assert hasattr(self.model, 'objects')


    def test_attribute_is_type_objects(self):
        """ Attribute Check

        attribute `objects` must be set to `access.models.TenancyManager()`
        """

        assert type(self.model.objects) is TenancyManager
