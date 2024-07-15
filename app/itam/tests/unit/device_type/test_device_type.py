import pytest
import unittest
import requests

from django.test import TestCase

from app.tests.abstract.models import TenancyModel

from itam.models.device import DeviceType


class DeviceTypeModel(
    TestCase,
    TenancyModel
):

    model = DeviceType
