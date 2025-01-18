import pytest

from django.conf import settings as django_settings
from django.shortcuts import reverse
from django.test import TestCase, Client

from app import settings





class SettingsDefault(TestCase):
    """ Test Settings file default values """


    def test_setting_default_debug_off(self):
        """ Ensure that debug is off within settings by default

            Debug is only required during development with this setting must always remain off within the committed code.
        """

        assert not settings.DEBUG


    def test_setting_default_debug_off_type(self):
        """ Settings attribute type check

        setting `DEBUG` must be of type bool
        """

        assert type(settings.DEBUG) is bool



    def test_setting_default_login_required(self):
        """ By default login should be required
        """

        assert settings.LOGIN_REQUIRED


    def test_setting_default_login_required_type(self):
        """ Settings attribute type check

        setting `LOGIN_REQUIRED` must be of type bool
        """

        assert type(settings.LOGIN_REQUIRED) is bool



    def test_setting_default_metrics_off(self):
        """ Ensure that metrics is off within settings by default

            Metrics is only required when user turns it on
        """

        assert not settings.METRICS_ENABLED


    def test_setting_default_metrics_off_type(self):
        """ Settings attribute type check

        setting `METRICS_ENABLED` must be of type bool
        """

        assert type(settings.METRICS_ENABLED) is bool



    def test_setting_default_use_tz(self):
        """ Ensure that 'USE_TZ = True' is within settings
        """

        assert settings.USE_TZ


    def test_setting_default_use_tz_type(self):
        """ Settings attribute type check

        setting `USE_TZ` must be of type bool
        """

        assert type(settings.USE_TZ) is bool



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



    def test_setting_value_metrics_off_middleware(self):
        """ Metrics off check

        when metrics are off, its middleware must not exist in settings
        """

        assert (
            'django_prometheus.middleware.PrometheusBeforeMiddleware' not in settings.MIDDLEWARE
                and
            'django_prometheus.middleware.PrometheusAfterMiddleware' not in settings.MIDDLEWARE
            )



    def test_setting_value_metrics_off_installed_apps(self):
        """  Metrics off check

        when metrics are off, it should not be installed.
        """

        assert 'django_prometheus' not in settings.INSTALLED_APPS


    @pytest.mark.skip( reason = 'figure out how to test' )
    def test_setting_value_metrics_on_middleware(self):
        """ Metrics off check

        logic in settings adjusts middleware when `METRICS_ENABLED=True`

        when metrics are off, its middleware must not exist in settings
        """

        assert (
            'django_prometheus.middleware.PrometheusBeforeMiddleware' in settings.MIDDLEWARE
                and
            'django_prometheus.middleware.PrometheusAfterMiddleware' in settings.MIDDLEWARE
            )



    @pytest.mark.skip( reason = 'figure out how to test' )
    def test_setting_value_metrics_on_installed_apps(self):
        """  Metrics off check

        logic in settings adjusts installed apps when `METRICS_ENABLED=True`

        when metrics are off, it should not be installed.
        """

        settings.METRICS_ENABLED = True

        assert 'django_prometheus' in settings.INSTALLED_APPS
