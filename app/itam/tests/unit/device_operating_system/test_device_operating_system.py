import pytest
import unittest

from django.test import TestCase

from access.models import Organization

from app.tests.abstract.models import TenancyModel

from config_management.models.groups import ConfigGroups, ConfigGroupSoftware

from itam.models.device import Device, DeviceOperatingSystem
from itam.models.operating_system import OperatingSystem, OperatingSystemVersion



class DeviceOperatingSystemModel(
    TestCase,
    TenancyModel,
):

    model = DeviceOperatingSystem



    @classmethod
    def setUpTestData(self):
        """ Setup Test

        """

        organization = Organization.objects.create(name='test_org')


        self.parent_item = Device.objects.create(
            organization=organization,
            name = 'device_name'
        )

        os = OperatingSystem.objects.create(
            organization=organization,
            name = 'os_name'
        )

        os_version = OperatingSystemVersion.objects.create(
            name = "12",
            operating_system = os,
        )


        self.item = self.model.objects.create(
            organization = organization,
            operating_system_version = os_version,
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
