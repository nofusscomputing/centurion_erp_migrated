import pytest
import unittest
import requests

from django.test import TestCase

from app.tests.abstract.models import TenancyModel

from core.models.manufacturer import Manufacturer


class ManufacturerModel(
    TestCase,
    TenancyModel
):

    model = Manufacturer
