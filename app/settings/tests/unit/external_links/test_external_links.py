import pytest
import unittest
import requests

from django.test import TestCase, Client

from app.tests.abstract.models import TenancyModel

from settings.models.external_link import ExternalLink



class ExternalLinkTests(
    TestCase,
    TenancyModel,
):

    model = ExternalLink
