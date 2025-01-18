import pytest

from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models import Organization

from app.tests.abstract.mock_view import MockView, User

from itim.serializers.port import Port, PortModelSerializer



class PortValidationAPI(
    TestCase,
):

    model = Port

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        # 2. Create an item
        """

        organization = Organization.objects.create(name='test_org')

        self.user = User.objects.create_user(username="test_user_view", password="password")

        self.organization = organization

        # self.item = self.model.objects.create(
        #     organization=organization,
        #     number = 'os name',
        # )

        self.mock_view = MockView( user = self.user )



    def test_serializer_validation_can_create(self):
        """Serializer Validation Check

        Ensure that a valid item has no validation errors
        """

        serializer = PortModelSerializer(
            context = {
                'request': self.mock_view.request,
                'view': self.mock_view,
            },
            data={
            "organization": self.organization.id,
            "number": 80,
            "protocol": Port.Protocol.TCP
        })

        assert serializer.is_valid(raise_exception = True)



    def test_serializer_validation_no_number(self):
        """Serializer Validation Check

        Ensure that if creating and no number is provided a validation error occurs
        """

        with pytest.raises(ValidationError) as err:

            serializer = PortModelSerializer(
                context = {
                'request': self.mock_view.request,
                'view': self.mock_view,
            },
            data={
                "organization": self.organization.id,
                # "number": 80,
                "protocol": Port.Protocol.TCP
            })

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['number'][0] == 'required'



    def test_serializer_validation_no_protocol(self):
        """Serializer Validation Check

        Ensure that if creating and no protocol is provided a validation error occurs
        """

        with pytest.raises(ValidationError) as err:

            serializer = PortModelSerializer(
                context = {
                    'request': self.mock_view.request,
                    'view': self.mock_view,
                },
                data={
                "organization": self.organization.id,
                "number": 80,
                # "protocol": Port.Protocol.TCP
            })

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['protocol'][0] == 'required'
