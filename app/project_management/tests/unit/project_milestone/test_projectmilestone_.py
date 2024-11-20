import pytest
# import unittest
# import requests

from django.test import TestCase

from access.models import Organization

from app.tests.abstract.models import TenancyModel

from project_management.models.project_milestone import Project, ProjectMilestone


class ProjectMilestoneModel(
    TestCase,
    TenancyModel
):

    model = ProjectMilestone


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a device
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.project = Project.objects.create(
            organization=organization,
            name = 'proj',
        )

        self.item = self.model.objects.create(
            organization=organization,
            name = 'mile',
            project = self.project
        )


    # def test_attribute_duration_ticket_value(self):
    #     """Attribute value test

    #     This aattribute calculates the ticket duration from
    #     it's comments. must return total time in seconds
    #     """

    #     pass