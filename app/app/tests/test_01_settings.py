from app import settings

import pytest
import unittest

class Test_aa_settings_default(unittest.TestCase):

    @pytest.mark.django_db
    def test_setting_api_disabled_default(self):
        """ As the API is only partially developed, it must be disabled.

            This test can be removed when the API has been fully developed and functioning as it should.
        """

        assert not settings.API_ENABLED


    @pytest.mark.django_db
    def test_setting_login_required_default(self):
        """ By default login should be required
        """

        assert settings.LOGIN_REQUIRED


    @pytest.mark.django_db
    def test_setting_use_tz_default(self):
        """ Ensure that 'USE_TZ = True' is within settings
        """

        assert settings.USE_TZ


    @pytest.mark.django_db
    def test_setting_debug_off(self):
        """ Ensure that debug is off within settings by default

            Debug is only required during development with this setting must always remain off within the committed code.
        """

        assert not settings.DEBUG
