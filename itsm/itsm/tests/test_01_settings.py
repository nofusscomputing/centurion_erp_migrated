from django.conf import settings

import pytest
import unittest

class Test_aa_settings_default(unittest.TestCase):

    @pytest.mark.django_db
    def test_setting_login_required_default(self):
        """ By default login should be required
        """

        assert settings.LOGIN_REQUIRED
