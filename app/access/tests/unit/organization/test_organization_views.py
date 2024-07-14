import pytest
import unittest
import requests

from django.test import TestCase

from app.tests.abstract.models import ModelDisplay, ModelIndex



class OrganizationViews(
    TestCase,
    ModelDisplay,
    ModelIndex
):

    display_module = 'access.views.organization'
    display_view = 'View'

    index_module = display_module
    index_view = 'IndexView'
