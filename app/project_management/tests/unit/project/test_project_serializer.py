import pytest

from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models import Organization

from project_management.serializers.project import (
    Project,
    ProjectModelSerializer
)



class ProjectValidationAPI(
    TestCase,
):

    model = Project

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        2. Create an item
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization



    def test_serializer_validation_can_create(self):
        """Serializer Validation Check

        Ensure that a valid item can be creates
        """

        serializer = ProjectModelSerializer(data={
            "organization": self.organization.id,
            "name": 'a project'
        })

        assert serializer.is_valid(raise_exception = True)



    def test_serializer_validation_no_name(self):
        """Serializer Validation Check

        Ensure that if creating and no name is provided a validation error occurs
        """

        with pytest.raises(ValidationError) as err:

            serializer = ProjectModelSerializer(
                data={
                    "organization": self.organization.id,
                },
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['name'][0] == 'required'



    def test_serializer_validation_external_ref_not_import_user(self):
        """Serializer Validation Check

        Ensure that if creating by user who is not import user, they can't edit
        fields external_ref and external_system.
        """

        class MockView:

            is_import_user = False


        serializer = ProjectModelSerializer(
            context = {
                'view': MockView
            },
            data={
                "name": 'a project name',
                "organization": self.organization.id,
                'external_ref': 1,
                'external_system': int(Project.Ticket_ExternalSystem.CUSTOM_1)
            },
        )

        serializer.is_valid(raise_exception = True)

        serializer.save()

        assert serializer.instance.external_ref is None and serializer.instance.external_system is None



    def test_serializer_validation_external_ref_is_import_user(self):
        """Serializer Validation Check

         Ensure that if creating by user who import user, they can edit
        fields external_ref and external_system.
        """

        class MockView:

            is_import_user = True


        serializer = ProjectModelSerializer(
            context = {
                'view': MockView
            },
            data={
                "name": 'a project name',
                "organization": self.organization.id,
                'external_ref': 1,
                'external_system': int(Project.Ticket_ExternalSystem.CUSTOM_1)
            },
        )

        serializer.is_valid(raise_exception = True)

        serializer.save()

        assert (
            serializer.instance.external_ref == 1 and 
            serializer.instance.external_system == int(Project.Ticket_ExternalSystem.CUSTOM_1)
        )
