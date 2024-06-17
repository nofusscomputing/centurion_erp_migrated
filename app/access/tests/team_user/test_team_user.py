import pytest
import unittest

from django.test import TestCase, Client
from django.contrib.auth.models import User

from access.models import Organization, Team, TeamUsers, Permission



class TeamUsersModel(TestCase):

    model = TeamUsers



    @classmethod
    def setUpTestData(self):
        """ Setup Test

        """

        organization = Organization.objects.create(name='test_org')

        different_organization = Organization.objects.create(name='test_different_organization')

        self.parent_item = Team.objects.create(
            team_name = 'test_team',
            organization = organization,
        )

        team_user = User.objects.create_user(username="test_self.team_user", password="password")

        self.item = self.model.objects.create(
            team = self.parent_item,
            user = team_user
        )



    def test_model_has_property_parent_object(self):
        """ Check if model contains 'parent_object'
        
            This is a required property for all models that have a parent
        """

        assert hasattr(self.model, 'parent_object')


    def test_model_property_parent_object_returns_object(self):
        """ Check if model contains 'parent_object'
        
            This is a required property for all models that have a parent
        """

        assert self.item.parent_object == self.parent_item
