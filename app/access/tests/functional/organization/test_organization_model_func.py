from django.contrib.auth.models import User
from django.test import TestCase

from access.models import Organization, Team, TeamUsers, Permission

from api.v2.tests.functional.abstract.test_model_functional import ModelAttributesFunctional



class Model(
    TestCase,
    ModelAttributesFunctional,
):

    model = Organization


    @classmethod
    def setUpTestData(self):

        self.view_user = User.objects.create_user(username="test_user_view", password="password", is_superuser=True)

        self.item = self.model.objects.create(name='test_org', manager=self.view_user)
