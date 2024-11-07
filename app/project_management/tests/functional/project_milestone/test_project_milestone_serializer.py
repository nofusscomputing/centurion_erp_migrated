import pytest

from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models import Organization

from project_management.serializers.project_milestone import (
    Project,
    ProjectMilestone,
    ProjectMilestoneModelSerializer
)



class ProjectMilestoneValidationAPI(
    TestCase,
):

    model = ProjectMilestone

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        2. Create an item
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.project = Project.objects.create(
            name = 'proj mile',
            organization = self.organization
        )



    def test_serializer_validation_can_create(self):
        """Serializer Validation Check

        Ensure that a valid item can be creates
        """

        # self._kwargs['context']['view'].kwargs['project_id'])

        class MockView:

            kwargs = {
                'project_id': self.project.id
            }

        serializer = ProjectMilestoneModelSerializer(
            context = {
                'view': MockView
            },
            data={
                "organization": self.organization.id,
                "name": 'a milestone',
            }
        )

        assert serializer.is_valid(raise_exception = True)



    def test_serializer_validation_no_name(self):
        """Serializer Validation Check

        Ensure that if creating and no name is provided a validation error occurs
        """

        class MockView:

            kwargs = {
                'project_id': self.project.id
            }

        with pytest.raises(ValidationError) as err:

            serializer = ProjectMilestoneModelSerializer(
                context = {
                    'view': MockView
                },
                data={
                    "organization": self.organization.id,
                },
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['name'][0] == 'required'



    # def test_serializer_validation_no_project(self):
    #     """Serializer Validation Check

    #     Ensure that if creating and no name is provided a validation error occurs
    #     """

    #     class MockView:

    #         kwargs = {
    #             'project_id': self.project.id
    #         }

    #     with pytest.raises(ValidationError) as err:

    #         serializer = ProjectMilestoneModelSerializer(
    #             context = {
    #                 'view': MockView
    #             },
    #             data={
    #                 "organization": self.organization.id,
    #                 "name": 'a milestone',
    #             },
    #         )

    #         serializer.is_valid(raise_exception = True)

    #     assert err.value.get_codes()['project'][0] == 'required'

