from django.conf import settings

import pytest
import unittest

class Test_aa_settings_default(unittest.TestCase):

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

