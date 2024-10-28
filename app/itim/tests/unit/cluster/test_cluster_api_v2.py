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

from itim.models.clusters import Cluster, ClusterType



class ClusterAPI(
    TestCase,
    APITenancyObject
):

    model = Cluster

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create an item

        """

        self.organization = Organization.objects.create(name='test_org')

        node = Device.objects.create(
            organization = self.organization,
            name = 'node',
        )

        device = Device.objects.create(
            organization = self.organization,
            name = 'device',
            is_virtual = True,
        )

        cluster_type = ClusterType.objects.create(
            organization = self.organization,
            name = 'cluster_type'
        )

        parent_cluster = Cluster.objects.create(
            organization = self.organization,
            name = 'two'
        )

        self.item = self.model.objects.create(
            organization = self.organization,
            name = 'one',
            cluster_type = cluster_type,
            config = dict({"one": "two"}),
            parent_cluster = parent_cluster,
            model_notes = 'a note'
        )

        self.item.devices.set([ device ])

        self.item.nodes.set([ node ])


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
        url = reverse('v2:_api_v2_cluster-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data = response.data


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


    def test_api_field_exists_resources(self):
        """ Test for existance of API Field

        resources field must exist
        """

        assert 'resources' in self.api_data


    def test_api_field_type_resources(self):
        """ Test for type for API Field

        resources field must be dict
        """

        assert type(self.api_data['resources']) is str



    def test_api_field_exists_nodes(self):
        """ Test for existance of API Field

        nodes field must exist
        """

        assert 'nodes' in self.api_data


    def test_api_field_type_nodes(self):
        """ Test for type for API Field

        nodes field must be dict
        """

        assert type(self.api_data['nodes'][0]) is dict


    def test_api_field_exists_nodes_id(self):
        """ Test for existance of API Field

        nodes.id field must exist
        """

        assert 'id' in self.api_data['nodes'][0]


    def test_api_field_type_nodes_id(self):
        """ Test for type for API Field

        nodes.id field must be int
        """

        assert type(self.api_data['nodes'][0]['id']) is int


    def test_api_field_exists_nodes_display_name(self):
        """ Test for existance of API Field

        nodes.display_name field must exist
        """

        assert 'display_name' in self.api_data['nodes'][0]


    def test_api_field_type_nodes_display_name(self):
        """ Test for type for API Field

        nodes.display_name field must be str
        """

        assert type(self.api_data['nodes'][0]['display_name']) is str


    def test_api_field_exists_nodes_url(self):
        """ Test for existance of API Field

        nodes.url field must exist
        """

        assert 'url' in self.api_data['nodes'][0]


    def test_api_field_type_nodes_url(self):
        """ Test for type for API Field

        nodes.url field must be Hyperlink
        """

        assert type(self.api_data['nodes'][0]['url']) is Hyperlink



    def test_api_field_exists_devices(self):
        """ Test for existance of API Field

        devices field must exist
        """

        assert 'devices' in self.api_data


    def test_api_field_type_devices(self):
        """ Test for type for API Field

        devices field must be list
        """

        assert type(self.api_data['devices']) is list


    def test_api_field_exists_devices_id(self):
        """ Test for existance of API Field

        devices.id field must exist
        """

        assert 'id' in self.api_data['devices'][0]


    def test_api_field_type_devices_id(self):
        """ Test for type for API Field

        devices.id field must be int
        """

        assert type(self.api_data['devices'][0]['id']) is int


    def test_api_field_exists_devices_display_name(self):
        """ Test for existance of API Field

        devices.display_name field must exist
        """

        assert 'display_name' in self.api_data['devices'][0]


    def test_api_field_type_devices_display_name(self):
        """ Test for type for API Field

        devices.display_name field must be str
        """

        assert type(self.api_data['devices'][0]['display_name']) is str


    def test_api_field_exists_devices_url(self):
        """ Test for existance of API Field

        devices.url field must exist
        """

        assert 'url' in self.api_data['devices'][0]


    def test_api_field_type_devices_url(self):
        """ Test for type for API Field

        devices.url field must be Hyperlink
        """

        assert type(self.api_data['devices'][0]['url']) is Hyperlink



    def test_api_field_exists_cluster_type(self):
        """ Test for existance of API Field

        cluster_type field must exist
        """

        assert 'cluster_type' in self.api_data


    def test_api_field_type_cluster_type(self):
        """ Test for type for API Field

        cluster_type field must be dict
        """

        assert type(self.api_data['cluster_type']) is dict


    def test_api_field_exists_cluster_type_id(self):
        """ Test for existance of API Field

        cluster_type.id field must exist
        """

        assert 'id' in self.api_data['cluster_type']


    def test_api_field_type_cluster_type_id(self):
        """ Test for type for API Field

        cluster_type.id field must be int
        """

        assert type(self.api_data['cluster_type']['id']) is int


    def test_api_field_exists_cluster_type_display_name(self):
        """ Test for existance of API Field

        cluster_type.display_name field must exist
        """

        assert 'display_name' in self.api_data['cluster_type']


    def test_api_field_type_cluster_type_display_name(self):
        """ Test for type for API Field

        cluster_type.display_name field must be str
        """

        assert type(self.api_data['cluster_type']['display_name']) is str


    def test_api_field_exists_cluster_type_url(self):
        """ Test for existance of API Field

        cluster_type.url field must exist
        """

        assert 'url' in self.api_data['cluster_type']


    def test_api_field_type_cluster_type_url(self):
        """ Test for type for API Field

        cluster_type.url field must be Hyperlink
        """

        assert type(self.api_data['cluster_type']['url']) is Hyperlink



    def test_api_field_exists_parent_cluster(self):
        """ Test for existance of API Field

        parent_cluster field must exist
        """

        assert 'parent_cluster' in self.api_data


    def test_api_field_type_parent_cluster(self):
        """ Test for type for API Field

        parent_cluster field must be dict
        """

        assert type(self.api_data['parent_cluster']) is dict


    def test_api_field_exists_parent_cluster_id(self):
        """ Test for existance of API Field

        parent_cluster.id field must exist
        """

        assert 'id' in self.api_data['parent_cluster']


    def test_api_field_type_parent_cluster_id(self):
        """ Test for type for API Field

        parent_cluster.id field must be int
        """

        assert type(self.api_data['parent_cluster']['id']) is int


    def test_api_field_exists_parent_cluster_display_name(self):
        """ Test for existance of API Field

        parent_cluster.display_name field must exist
        """

        assert 'display_name' in self.api_data['parent_cluster']


    def test_api_field_type_parent_cluster_display_name(self):
        """ Test for type for API Field

        parent_cluster.display_name field must be str
        """

        assert type(self.api_data['parent_cluster']['display_name']) is str


    def test_api_field_exists_parent_cluster_url(self):
        """ Test for existance of API Field

        parent_cluster.url field must exist
        """

        assert 'url' in self.api_data['parent_cluster']


    def test_api_field_type_parent_cluster_url(self):
        """ Test for type for API Field

        parent_cluster.url field must be Hyperlink
        """

        assert type(self.api_data['parent_cluster']['url']) is Hyperlink



    def test_api_field_exists_urls_tickets(self):
        """ Test for existance of API Field

        _urls.tickets field must exist
        """

        assert 'tickets' in self.api_data['_urls']


    def test_api_field_type_urls_tickets(self):
        """ Test for type for API Field

        _urls.tickets field must be str
        """

        assert type(self.api_data['_urls']['tickets']) is str
