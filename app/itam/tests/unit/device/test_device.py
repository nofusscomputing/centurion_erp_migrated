# from django.conf import settings
# from django.shortcuts import reverse
from django.test import TestCase, Client

import pytest
import unittest
import requests

from app.tests.abstract.models import TenancyModel

from itam.models.device import Device


class Device(
    TestCase,
    TenancyModel,
):

    model = Device

    # @classmethod
    # def setUpTestData(self):
    #     """Setup Test

    #     1. Create an organization for user and item
    #     . create an organization that is different to item
    #     2. Create a device
    #     3. create teams with each permission: view, add, change, delete
    #     4. create a user per team
    #     """

    #     organization = Organization.objects.create(name='test_org')

    #     self.organization = organization

    #     self.item = self.model.objects.create(
    #         organization=organization,
    #         name = 'deviceone'
    #     )

    @pytest.mark.skip(reason="to be written")
    def test_device_move_organization(user):
        """Move Organization test

        When a device moves organization, devicesoftware and devicesoftware table data
        must also move organizations
        """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_device_software_action(user):
        """Ensure only software that is from the same organization or is global can be added to the device
        """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_device_not_global(user):
        """Devices are not global items.

            Ensure that a device can't be set to be global.
        """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_device_operating_system_version_only_one(user):
        """model deviceoperatingsystem must only contain one value per device
        """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_device_device_model_same_organization(user):
        """ Can only add a device model from same organization """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_device_device_model_global(user):
        """ Can add a device model that is set is_global=true """
        pass
