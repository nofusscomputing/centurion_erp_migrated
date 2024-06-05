import pytest
import unittest

from django.test import TestCase

from config_management.models.groups import ConfigGroups


class ConfigGroups(TestCase):

    model = ConfigGroups

    model_name = 'configgroups'


    @pytest.mark.skip(reason="to be written")
    def test_config_groups_config_keys_valid_ansible_variable():
        """ All config keys must be valid ansible variables """
        pass

