import pytest
import unittest

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from rest_framework.relations import Hyperlink

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_fields import APITenancyObject

from itam.models.device import Device

from itim.models.clusters import Cluster
from itim.models.services import Service, Port



class ServiceAPI(
    TestCase,
    APITenancyObject
):

    model = Service

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create an item

        """

        self.organization = Organization.objects.create(name='test_org')

        port = Port.objects.create(
            organization = self.organization,
            number = 80,
            protocol = Port.Protocol.TCP
        )

        device = Device.objects.create(
            organization = self.organization,
            name = 'device-one'
        )


        cluster = Cluster.objects.create(
            organization = self.organization,
            name = 'cluster one'
        )


        dependent_service = self.model.objects.create(
            organization = self.organization,
            name = 'one',
        )

        self.item = self.model.objects.create(
            organization = self.organization,
            name = 'one',
            model_notes = 'a note',
            device = device,
            config = dict({ "one": "two"}),
            is_template = True,
            config_key_variable = 'boo'
        )

        self.item_two = self.model.objects.create(
            organization = self.organization,
            name = 'one',
            model_notes = 'a note',
            cluster = cluster,
            template = self.item
        )


        self.item.port.set([ port ])

        self.item.dependent_service.set([ dependent_service ])


        self.url_view_kwargs = {'pk': self.item.id}

        view_permissions = Permission.objects.get(
                codename = 'view_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        view_team = Team.objects.create(
            team_name = 'view_team',
            organization = self.organization,
        )

        view_team.permissions.set([view_permissions])

        self.view_user = User.objects.create_user(username="test_user_view", password="password")
        teamuser = TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )

        client = Client()
        url = reverse('API:_api_v2_service-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data = response.data


        url = reverse('API:_api_v2_service-detail', kwargs={'pk': self.item_two.id})

        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data_two = response.data



    def test_api_field_exists_config(self):
        """ Test for existance of API Field

        config field must exist
        """

        assert 'config' in self.api_data


    def test_api_field_type_config(self):
        """ Test for type for API Field

        config field must be dict
        """

        assert type(self.api_data['config']) is dict



    def test_api_field_exists_rendered_config(self):
        """ Test for existance of API Field

        rendered_config field must exist
        """

        assert 'rendered_config' in self.api_data


    def test_api_field_type_rendered_config(self):
        """ Test for type for API Field

        rendered_config field must be dict
        """

        assert type(self.api_data['rendered_config']) is dict



    def test_api_field_exists_is_template(self):
        """ Test for existance of API Field

        is_template field must exist
        """

        assert 'is_template' in self.api_data


    def test_api_field_type_is_template(self):
        """ Test for type for API Field

        is_template field must be bool
        """

        assert type(self.api_data['is_template']) is bool



    def test_api_field_exists_template(self):
        """ Test for existance of API Field

        template field must exist
        """

        assert 'template' in self.api_data_two


    def test_api_field_type_template(self):
        """ Test for type for API Field

        template field must be dict
        """

        assert type(self.api_data_two['template']) is dict



    def test_api_field_exists_template_id(self):
        """ Test for existance of API Field

        template.id field must exist
        """

        assert 'id' in self.api_data_two['template']


    def test_api_field_type_template_id(self):
        """ Test for type for API Field

        template.id field must be int
        """

        assert type(self.api_data_two['template']['id']) is int


    def test_api_field_exists_template_display_name(self):
        """ Test for existance of API Field

        template.display_name field must exist
        """

        assert 'display_name' in self.api_data_two['template']


    def test_api_field_type_template_display_name(self):
        """ Test for type for API Field

        template.display_name field must be str
        """

        assert type(self.api_data_two['template']['display_name']) is str


    def test_api_field_exists_template_url(self):
        """ Test for existance of API Field

        template.url field must exist
        """

        assert 'url' in self.api_data_two['template']


    def test_api_field_type_template_url(self):
        """ Test for type for API Field

        template.url field must be Hyperlink
        """

        assert type(self.api_data_two['template']['url']) is Hyperlink



    def test_api_field_exists_config_key_variable(self):
        """ Test for existance of API Field

        config_key_variable field must exist
        """

        assert 'config_key_variable' in self.api_data


    def test_api_field_type_config_key_variable(self):
        """ Test for type for API Field

        config_key_variable field must be str
        """

        assert type(self.api_data['config_key_variable']) is str



    def test_api_field_exists_dependent_service(self):
        """ Test for existance of API Field

        dependent_service field must exist
        """

        assert 'dependent_service' in self.api_data


    def test_api_field_type_dependent_service(self):
        """ Test for type for API Field

        dependent_service field must be list
        """

        assert type(self.api_data['dependent_service']) is list



    def test_api_field_exists_dependent_service_id(self):
        """ Test for existance of API Field

        dependent_service.id field must exist
        """

        assert 'id' in self.api_data['dependent_service'][0]


    def test_api_field_type_dependent_service_id(self):
        """ Test for type for API Field

        dependent_service.id field must be int
        """

        assert type(self.api_data['dependent_service'][0]['id']) is int


    def test_api_field_exists_dependent_service_display_name(self):
        """ Test for existance of API Field

        dependent_service.display_name field must exist
        """

        assert 'display_name' in self.api_data['dependent_service'][0]


    def test_api_field_type_dependent_service_display_name(self):
        """ Test for type for API Field

        dependent_service.display_name field must be str
        """

        assert type(self.api_data['dependent_service'][0]['display_name']) is str


    def test_api_field_exists_dependent_service_url(self):
        """ Test for existance of API Field

        dependent_service.url field must exist
        """

        assert 'url' in self.api_data['dependent_service'][0]


    def test_api_field_type_dependent_service_url(self):
        """ Test for type for API Field

        dependent_service.url field must be Hyperlink
        """

        assert type(self.api_data['dependent_service'][0]['url']) is Hyperlink



    def test_api_field_exists_port(self):
        """ Test for existance of API Field

        port field must exist
        """

        assert 'port' in self.api_data


    def test_api_field_type_port(self):
        """ Test for type for API Field

        port field must be list
        """

        assert type(self.api_data['port']) is list



    def test_api_field_exists_port_id(self):
        """ Test for existance of API Field

        port.id field must exist
        """

        assert 'id' in self.api_data['port'][0]


    def test_api_field_type_port_id(self):
        """ Test for type for API Field

        port.id field must be int
        """

        assert type(self.api_data['port'][0]['id']) is int


    def test_api_field_exists_port_display_name(self):
        """ Test for existance of API Field

        port.display_name field must exist
        """

        assert 'display_name' in self.api_data['port'][0]


    def test_api_field_type_port_display_name(self):
        """ Test for type for API Field

        port.display_name field must be str
        """

        assert type(self.api_data['port'][0]['display_name']) is str


    def test_api_field_exists_port_url(self):
        """ Test for existance of API Field

        port.url field must exist
        """

        assert 'url' in self.api_data['port'][0]


    def test_api_field_type_port_url(self):
        """ Test for type for API Field

        port.url field must be Hyperlink
        """

        assert type(self.api_data['port'][0]['url']) is Hyperlink



    def test_api_field_exists_device(self):
        """ Test for existance of API Field

        device field must exist
        """

        assert 'device' in self.api_data


    def test_api_field_type_device(self):
        """ Test for type for API Field

        device field must be dict
        """

        assert type(self.api_data['device']) is dict



    def test_api_field_exists_device_id(self):
        """ Test for existance of API Field

        device.id field must exist
        """

        assert 'id' in self.api_data['device']


    def test_api_field_type_device_id(self):
        """ Test for type for API Field

        device.id field must be int
        """

        assert type(self.api_data['device']['id']) is int


    def test_api_field_exists_device_display_name(self):
        """ Test for existance of API Field

        device.display_name field must exist
        """

        assert 'display_name' in self.api_data['device']


    def test_api_field_type_device_display_name(self):
        """ Test for type for API Field

        device.display_name field must be str
        """

        assert type(self.api_data['device']['display_name']) is str


    def test_api_field_exists_device_url(self):
        """ Test for existance of API Field

        device.url field must exist
        """

        assert 'url' in self.api_data['device']


    def test_api_field_type_device_url(self):
        """ Test for type for API Field

        device.url field must be Hyperlink
        """

        assert type(self.api_data['device']['url']) is Hyperlink



    def test_api_field_exists_cluster(self):
        """ Test for existance of API Field

        cluster field must exist
        """

        assert 'cluster' in self.api_data_two


    def test_api_field_type_cluster(self):
        """ Test for type for API Field

        cluster field must be list
        """

        assert type(self.api_data_two['cluster']) is dict



    def test_api_field_exists_cluster_id(self):
        """ Test for existance of API Field

        cluster.id field must exist
        """

        assert 'id' in self.api_data_two['cluster']


    def test_api_field_type_cluster_id(self):
        """ Test for type for API Field

        cluster.id field must be int
        """

        assert type(self.api_data_two['cluster']['id']) is int


    def test_api_field_exists_cluster_display_name(self):
        """ Test for existance of API Field

        cluster.display_name field must exist
        """

        assert 'display_name' in self.api_data_two['cluster']


    def test_api_field_type_cluster_display_name(self):
        """ Test for type for API Field

        cluster.display_name field must be str
        """

        assert type(self.api_data_two['cluster']['display_name']) is str


    def test_api_field_exists_cluster_url(self):
        """ Test for existance of API Field

        cluster.url field must exist
        """

        assert 'url' in self.api_data_two['cluster']


    def test_api_field_type_cluster_url(self):
        """ Test for type for API Field

        cluster.url field must be Hyperlink
        """

        assert type(self.api_data_two['cluster']['url']) is Hyperlink
