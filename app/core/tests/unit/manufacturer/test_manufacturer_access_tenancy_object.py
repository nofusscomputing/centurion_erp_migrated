import pytest
import unittest
import requests

from django.test import TestCase, Client

from access.tests.abstract.tenancy_object import TenancyObject

from core.models.manufacturer import Manufacturer



class ManufacturerTenancyObject(
    TestCase,
    TenancyObject
):

    model = Manufacturer
