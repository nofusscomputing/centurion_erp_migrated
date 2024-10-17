import pytest

from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models import Organization

from config_management.serializers.config_group_software import ConfigGroupSoftware, ConfigGroupSoftwareModelSerializer
from config_management.models.groups import ConfigGroups

from itam.models.software import Software, SoftwareVersion



class ConfigGroupSoftwareValidationAPI(
    TestCase,
):

    model = ConfigGroupSoftware


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        2. create software
        3. create software version
        4. create config group
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.software = Software.objects.create(
            organization=organization,
            name = 'software config'
        )

        self.software_version = SoftwareVersion.objects.create(
            organization=organization,
            software = self.software,
            name = '1.2.2'
        )



        self.software_two = Software.objects.create(
            organization=organization,
            name = 'software config two'
        )

        self.software_version_two = SoftwareVersion.objects.create(
            organization=organization,
            software = self.software_two,
            name = '1.2.3'
        )



        self.config_group = ConfigGroups.objects.create(
            organization=organization,
            name = 'random title',
            config = { 'config_key': 'a value' }
        )

        self.config_group_already_has_software = ConfigGroups.objects.create(
            organization=organization,
            name = 'random title',
            config = { 'config_key': 'a value' }
        )

        self.config_group_software = ConfigGroupSoftware.objects.create(
            organization=organization,
            config_group = self.config_group_already_has_software,
            software = self.software,
            version = self.software_version
        )



    # def test_serializer_validation_no_name(self):
    #     """Serializer Validation Check

    #     Ensure that if creating and no name is provided a validation error occurs
    #     """

    #     with pytest.raises(ValidationError) as err:

    #         serializer = ConfigGroupModelSerializer(data={
    #             "organization": self.organization.id,
    #         })

    #         serializer.is_valid(raise_exception = True)

    #     assert err.value.get_codes()['name'][0] == 'required'



    def test_serializer_validation_update_existing_software_add_same(self):
        """Serializer Validation Check

        Ensure that if an existing item is already assigned a piece of software
        and an attempt to reassign the same software it raises a validation error
        """

        with pytest.raises(ValidationError) as err:

            serializer = ConfigGroupSoftwareModelSerializer(
                self.config_group_software,
                data={
                    "software": self.software.id
                },
                partial=True,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['software'][0] == 'software_exists'



    def test_serializer_validation_update_version_not_exist(self):
        """Serializer Validation Check

        Ensure that if an existing item is assigned a piece of software that doesn't
        exist, it raises a validation error
        """

        with pytest.raises(ValidationError) as err:

            serializer = ConfigGroupSoftwareModelSerializer(
                self.config_group_software,
                data={
                    "version": 55
                },
                partial=True,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['version'][0] == 'does_not_exist'



    def test_serializer_validation_update_version_from_other_software(self):
        """Serializer Validation Check

        Ensure that if an existing item is assigned a piece of software is assigned a
        software version from a different piece of software, it raises a validation error
        """

        with pytest.raises(ValidationError) as err:

            serializer = ConfigGroupSoftwareModelSerializer(
                self.config_group_software,
                data={
                    "version": self.software_version_two.id
                },
                partial=True,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['version'][0] == 'software_not_own_version'


    # def test_serializer_validation_update_existing_invalid_config_key(self):
    #     """Serializer Validation Check

    #     Ensure that if an existing item has it's config updated with an invalid config key
    #     a validation exception is raised.
    #     """

    #     invalid_config = self.item_no_parent.config.copy()
    #     invalid_config.update({ 'software': 'is invalid' })

    #     with pytest.raises(ValidationError) as err:

    #         serializer = ConfigGroupModelSerializer(
    #             self.item_no_parent,
    #             data={
    #                 "config": invalid_config
    #             },
    #             partial=True,
    #         )

    #         serializer.is_valid(raise_exception = True)

    #     assert err.value.get_codes()['config'][0] == 'invalid'
