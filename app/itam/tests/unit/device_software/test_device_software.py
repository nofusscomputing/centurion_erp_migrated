import pytest
import unittest

from django.test import TestCase

from access.models import Organization

from app.tests.abstract.models import TenancyModel

from config_management.models.groups import ConfigGroups, ConfigGroupSoftware

from itam.models.device import Device, DeviceSoftware
from itam.models.software import Software



class DeviceSoftwareModel(
    TestCase,
    TenancyModel,
):

    model = DeviceSoftware


    @classmethod
    def setUpTestData(self):
        """ Setup Test

        """

        organization = Organization.objects.create(name='test_org')


        self.parent_item = Device.objects.create(
            organization=organization,
            name = 'device_name'
        )

        self.software_item = Software.objects.create(
            organization=organization,
            name = 'software_name',
        )

        self.item = self.model.objects.create(
            software = self.software_item,
            device = self.parent_item
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
