import pytest
import unittest
import requests

from django.test import TestCase

from app.tests.abstract.models import TenancyModel

from itam.models.software import SoftwareVersion



class SoftwareVersionModel(
    TestCase,
    TenancyModel
):

    model = SoftwareVersion
