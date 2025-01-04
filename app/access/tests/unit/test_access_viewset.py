from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import Client, TestCase

from rest_framework.permissions import IsAuthenticated

from access.models import Organization

from api.tests.abstract.viewsets import ViewSetCommon

from access.viewsets.index import Index


class AccessViewset(
    TestCase,
    ViewSetCommon
):

    viewset = Index

    route_name = 'API:_api_v2_access_home'


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user
        3. create super user
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.view_user = User.objects.create_user(username="test_user_add", password="password", is_superuser=True)


        client = Client()
        url = reverse(self.route_name + '-list')


        client.force_login(self.view_user)
        self.http_options_response_list = client.options(url)



    def test_view_attr_permission_classes_value(self):
        """Attribute Test

        Attribute `permission_classes` must be metadata class `ReactUIMetadata`
        """

        view_set = self.viewset()

        assert view_set.permission_classes[0] is IsAuthenticated

        assert len(view_set.permission_classes) == 1
