from django.conf import settings as django_settings
from django.shortcuts import reverse
from django.test import TestCase, Client

from app import settings


import pytest
import unittest


class SettingsDefault(TestCase):
    """ Test Settings file default values """


    def test_setting_default_login_required(self):
        """ By default login should be required
        """

        assert settings.LOGIN_REQUIRED


    def test_setting_default_use_tz(self):
        """ Ensure that 'USE_TZ = True' is within settings
        """

        assert settings.USE_TZ


    def test_setting_default_debug_off(self):
        """ Ensure that debug is off within settings by default

            Debug is only required during development with this setting must always remain off within the committed code.
        """

        assert not settings.DEBUG



class SettingsValues(TestCase):
    """ Test Each setting that offers different functionality """


    def test_setting_value_login_required(self):
        """Some docstring defining what the test is checking."""
        client = Client()
        url = reverse('home')

        django_settings.LOGIN_REQUIRED = True

        response = client.get(url)

        assert response.status_code == 302 and response.url.startswith('/account/login')



    def test_setting_value_login_required_not(self):
        """Some docstring defining what the test is checking."""
        client = Client()
        url = reverse('home')
        
        django_settings.LOGIN_REQUIRED = False

        response = client.get(url)

        assert response.status_code == 200
