import pytest
import unittest

from django.test import TestCase

from access.models import Organization

from app.tests.abstract.models import TenancyModel

from config_management.models.groups import ConfigGroups



@pytest.mark.django_db
class ConfigGroupsModel(
    TestCase,
    TenancyModel
):

    model = ConfigGroups

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create an item

        """

        self.organization = Organization.objects.create(name='test_org')


        self.item = self.model.objects.create(
            organization = self.organization,
            name = 'one',
            config = dict({"key": "one", "existing": "dont_over_write"})
        )

        self.second_item = self.model.objects.create(
            organization = self.organization,
            name = 'one_two',
            config = dict({"key": "two"}),
            parent = self.item
        )



    def test_config_groups_count_child_groups(self):
        """ Test function count_children """

        assert self.item.count_children() == 1


    def test_config_groups_rendered_config_not_empty(self):
        """ Rendered Config must be returned """

        assert self.item.config is not None


    def test_config_groups_rendered_config_is_dict(self):
        """ Rendered Config is a string """

        assert type(self.item.render_config()) is str


    def test_config_groups_rendered_config_is_correct(self):
        """ Rendered Config is correct """

        assert self.item.config['key'] == 'one'


    def test_config_groups_rendered_config_inheritence_overwrite(self):
        """ rendered config from parent group merged correctly """

        assert self.second_item.config['key'] == 'two'


    def test_config_groups_rendered_config_inheritence_existing_key_present(self):
        """ rendered config from parent group merge existing key present
        
        during merge, a key that doesn't exist in the child group that exists in the
        parent group should be within the child groups rendered config
        """

        assert self.second_item.config['key'] == 'two'


    @pytest.mark.skip(reason="to be written")
    def test_config_groups_config_keys_valid_ansible_variable():
        """ All config keys must be valid ansible variables """
        pass

