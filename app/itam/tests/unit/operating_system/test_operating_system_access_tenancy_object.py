import pytest
import unittest
import requests

from django.test import TestCase, Client

from access.tests.abstract.tenancy_object import TenancyObject

from itam.models.operating_system import OperatingSystem



class OperatingSystemTenancyObject(
    TestCase,
    TenancyObject
):

    model = OperatingSystem
