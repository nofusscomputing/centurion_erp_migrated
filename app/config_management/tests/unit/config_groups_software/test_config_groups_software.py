import pytest
import unittest

from django.test import TestCase

from access.models import Organization

from app.tests.abstract.models import TenancyModel

from config_management.models.groups import ConfigGroups, ConfigGroupSoftware

from itam.models.device import DeviceSoftware
from itam.models.software import Software



class ConfigGroupSoftwareModel(
    TestCase,
    TenancyModel
):

    model = ConfigGroupSoftware


    @classmethod
    def setUpTestData(self):
        """ Setup Test

        """

        organization = Organization.objects.create(name='test_org')


        self.parent_item = ConfigGroups.objects.create(
            organization=organization,
            name = 'group_one'
        )

        self.software_item = Software.objects.create(
            organization=organization,
            name = 'softwareone',
        )

        self.item = self.model.objects.create(
            organization = organization,
            software = self.software_item,
            config_group = self.parent_item,
            action = DeviceSoftware.Actions.INSTALL
        )



    def test_model_has_property_parent_object(self):
        """ Check if model contains 'parent_object'
        
            This is a required property for all models that have a parent
        """

        assert hasattr(self.model, 'parent_object')


    def test_model_property_parent_object_returns_object(self):
        """ Check if model contains 'parent_object'
        
            This is a required property for all models that have a parent
        """

        assert self.item.parent_object == self.parent_item
