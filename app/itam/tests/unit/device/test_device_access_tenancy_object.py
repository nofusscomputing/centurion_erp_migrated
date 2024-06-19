import pytest
import unittest

from django.test import TestCase, Client

from access.tests.abstract.tenancy_object import TenancyObject

from itam.models.device import Device



class DeviceTenancyObject(
    TestCase,
    TenancyObject
):

    model = Device

