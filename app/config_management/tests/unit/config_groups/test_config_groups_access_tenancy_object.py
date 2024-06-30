import pytest
import unittest
import requests

from django.test import TestCase, Client

from access.tests.abstract.tenancy_object import TenancyObject

from config_management.models.groups import ConfigGroups



class ConfigGroupsTenancyObject(
    TestCase,
    TenancyObject
):

    model = ConfigGroups
