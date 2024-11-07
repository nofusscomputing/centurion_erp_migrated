import pytest

from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models import Organization

from itim.serializers.cluster import Cluster, ClusterModelSerializer



class ClusterValidationAPI(
    TestCase,
):

    model = Cluster

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        2. Create an item
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.item = self.model.objects.create(
            organization=organization,
            name = 'os name',
        )



    def test_serializer_validation_no_name(self):
        """Serializer Validation Check

        Ensure that if creating and no name is provided a validation error occurs
        """

        with pytest.raises(ValidationError) as err:

            serializer = ClusterModelSerializer(data={
                "organization": self.organization.id,
            })

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['name'][0] == 'required'



    def test_serializer_validation_self_not_parent(self):
        """Serializer Validation Check

        Ensure that if assiging itself as parent a validation error occurs
        """

        with pytest.raises(ValidationError) as err:

            serializer = ClusterModelSerializer(
                self.item,
                data={
                    "parent_cluster": self.item.id,
                },
                partial = True
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['parent_cluster'] == 'parent_not_self'
