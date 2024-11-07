import pytest

from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models import Organization

from itam.models.device import Device

from itim.models.services import Port

from itim.models.clusters import Cluster
from itim.serializers.service import Service, ServiceModelSerializer



class ServiceValidationAPI(
    TestCase,
):

    model = Service

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        2. Create an item
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization


        self.port = Port.objects.create(
            organization = self.organization,
            number = 80,
            protocol = Port.Protocol.TCP
        )

        self.device = Device.objects.create(
            organization = self.organization,
            name = 'a-device'
        )

        self.cluster = Cluster.objects.create(
            organization = self.organization,
            name = 'a cluster'
        )


        self.item = self.model.objects.create(
            organization=organization,
            name = 'os name',
            cluster = self.cluster,
            config_key_variable = 'value'
        )

        self.item_two = self.model.objects.create(
            organization=organization,
            name = 'os name',
            cluster = self.cluster,
        )

        self.item_two.dependent_service.set([ self.item ])


        self.item_is_template = self.model.objects.create(
            organization=organization,
            name = 'os name',
            is_template = True,
        )

        self.item_is_template.port.set([ self.port ])


        self.item_is_template_no_port = self.model.objects.create(
            organization=organization,
            name = 'os name',
            is_template = True,
        )




    def test_serializer_validation_can_create_device(self):
        """Serializer Validation Check

        Ensure that a valid item is serialized
        """

        serializer = ServiceModelSerializer(
            data={
                'organization': self.organization.id,
                'name': 'service',
                'port': [
                    self.port.id
                ],
                'config_key_variable': 'a_key',
                'device': self.device.id
            },
        )

        assert serializer.is_valid(raise_exception = True)



    def test_serializer_validation_can_create_cluster(self):
        """Serializer Validation Check

        Ensure that a valid item is serialized
        """

        serializer = ServiceModelSerializer(
            data={
                'organization': self.organization.id,
                'name': 'service',
                'port': [
                    self.port.id
                ],
                'config_key_variable': 'a_key',
                'cluster': self.cluster.id
            },
        )

        assert serializer.is_valid(raise_exception = True)



    def test_serializer_validation_no_name(self):
        """Serializer Validation Check

        Ensure that if creating and no name is provided a validation error occurs
        """

        with pytest.raises(ValidationError) as err:

            serializer = ServiceModelSerializer(data={
                'organization': self.organization.id,
                'port': [
                    self.port.id
                ],
                'config_key_variable': 'a_key',
                'device': self.device.id
            })

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['name'][0] == 'required'



    def test_serializer_validation_no_port(self):
        """Serializer Validation Check

        Ensure that if creating and no port is provided a validation error occurs
        """

        with pytest.raises(ValidationError) as err:

            serializer = ServiceModelSerializer(data={
                'organization': self.organization.id,
                'name': 'service',
                'config_key_variable': 'a_key',
                'device': self.device.id
            })

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['port'][0] == 'required'



    def test_serializer_validation_no_port_required_if_template_with_port(self):
        """Serializer Validation Check

        Ensure that if creating and no port is provided and the template has a port
        no validation error occurs
        """

        serializer = ServiceModelSerializer(data={
            'organization': self.organization.id,
            'name': 'service',
            'config_key_variable': 'a_key',
            'device': self.device.id,
            'template': self.item_is_template.id
        })

        assert serializer.is_valid(raise_exception = True)



    def test_serializer_validation_template_without_port(self):
        """Serializer Validation Check

        Ensure that if creating a port is provided and the template has no port
        no validation error occurs
        """

        serializer = ServiceModelSerializer(data={
            'organization': self.organization.id,
            'name': 'service',
            'port': [
                self.port.id
            ],
            'config_key_variable': 'a_key',
            'device': self.device.id,
            'template': self.item_is_template_no_port.id
        })

        assert serializer.is_valid(raise_exception = True)



    def test_serializer_validation_no_port_or_template_port(self):
        """Serializer Validation Check

        Ensure that if creating and no port is provided and the template
        has no port a validation error occurs
        """

        with pytest.raises(ValidationError) as err:

            serializer = ServiceModelSerializer(data={
                'organization': self.organization.id,
                'name': 'service',
                'config_key_variable': 'a_key',
                'device': self.device.id,
                'template': self.item_is_template_no_port.id
            })

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['port'][0] == 'required'



    def test_serializer_validation_no_device(self):
        """Serializer Validation Check

        Ensure that if creating and no device is provided a validation error occurs
        """

        with pytest.raises(ValidationError) as err:

            serializer = ServiceModelSerializer(data={
                'organization': self.organization.id,
                'name': 'service',
                'port': [
                    self.port.id
                ],
                'config_key_variable': 'a_key',
            })

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['non_field_errors'][0] == 'one_of_cluster_or_device'



    def test_serializer_validation_device_and_cluster(self):
        """Serializer Validation Check

        Ensure that if creating and a cluster and device is provided
        a validation error occurs
        """

        with pytest.raises(ValidationError) as err:

            serializer = ServiceModelSerializer(data={
                'organization': self.organization.id,
                'name': 'service',
                'port': [
                    self.port.id
                ],
                'config_key_variable': 'a_key',
                'device': self.device.id,
                'cluster': self.cluster.id
            })

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['non_field_errors'][0] == 'either_cluster_or_device'



    def test_serializer_validation_no_circular_dependency(self):
        """Serializer Validation Check

        Ensure that if creating and a dependent service loop
        a validation error occurs
        """

        with pytest.raises(ValidationError) as err:

            serializer = ServiceModelSerializer(
                self.item,
                data={
                    'dependent_service': [
                        self.item_two.id
                    ],
                },
                partial = True
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['dependent_service'][0] == 'no_circular_dependencies'
