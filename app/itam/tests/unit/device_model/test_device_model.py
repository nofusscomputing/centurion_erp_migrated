import pytest
import unittest
import requests

from django.test import TestCase, Client

from app.tests.abstract.models import TenancyModel

from itam.models.device_models import DeviceModel



class DeviceModelModel(
    TestCase,
    TenancyModel
):

    model = DeviceModel

    @pytest.mark.skip(reason="to be written")
    def test_device_model_software_action(user):
        """Ensure only software that is from the same organization or is global can be added to the device
        """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_device_model_must_have_organization(user):
        """ Device Model must have organization set """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_device_model_not_global(user):
        """Devices are not global items.

            Ensure that a device can't be set to be global.
        """
        pass


    @pytest.mark.skip(reason="to be written")
    def test_device_model_operating_system_version_only_one(user):
        """model deviceoperatingsystem must only contain one value per device
        """
        pass
