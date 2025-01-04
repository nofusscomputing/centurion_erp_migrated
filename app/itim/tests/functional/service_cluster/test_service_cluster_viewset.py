import pytest

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_permissions_viewset import APIPermissionView
from api.tests.abstract.api_serializer_viewset import SerializerView
from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional, MetaDataNavigationEntriesFunctional

from itim.models.clusters import Cluster
from itim.models.services import Service, Port



class ViewSetBase:

    model = Service

    app_namespace = 'v2'
    
    url_name = '_api_v2_service_cluster'

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a team
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        different_organization = Organization.objects.create(name='test_different_organization')

        self.different_organization = different_organization


        view_permissions = Permission.objects.get(
                codename = 'view_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        view_team = Team.objects.create(
            team_name = 'view_team',
            organization = organization,
        )

        view_team.permissions.set([view_permissions])



        add_permissions = Permission.objects.get(
                codename = 'add_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )


        change_permissions = Permission.objects.get(
                codename = 'change_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )



        delete_permissions = Permission.objects.get(
                codename = 'delete_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )



        self.no_permissions_user = User.objects.create_user(username="test_no_permissions", password="password")


        self.view_user = User.objects.create_user(username="test_user_view", password="password")
        teamuser = TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )

        cluster = Cluster.objects.create(
            organization=organization,
            name = 'cluster'
        )

        port = Port.objects.create(
            organization=organization,
            number = 80,
            protocol = Port.Protocol.TCP
        )

        self.item = self.model.objects.create(
            organization=organization,
            name = 'os name',
            cluster = cluster,
            config_key_variable = 'value'
        )

        self.other_org_item = self.model.objects.create(
            organization=different_organization,
            name = 'os name b',
            cluster = cluster,
            config_key_variable = 'values'
        )

        self.item.port.set([ port ])



        self.url_view_kwargs = {'cluster_id': cluster.id, 'pk': self.item.id}

        self.url_kwargs = {'cluster_id': cluster.id}


        self.different_organization_user = User.objects.create_user(username="test_different_organization_user", password="password")


        different_organization_team = Team.objects.create(
            team_name = 'different_organization_team',
            organization = different_organization,
        )

        different_organization_team.permissions.set([
            view_permissions,
            add_permissions,
            change_permissions,
            delete_permissions,
        ])

        TeamUsers.objects.create(
            team = different_organization_team,
            user = self.different_organization_user
        )



class ServicePermissionsAPI(ViewSetBase, APIPermissionView, TestCase):


    def test_returned_data_from_user_and_global_organizations_only(self):
        """Check items returned

        This test case is a over-ride of a test case with the same name.
        This model is not a tenancy model making this test not-applicable.

        Items returned from the query Must be from the users organization and
        global ONLY!
        """
        pass




class ServiceViewSet(ViewSetBase, SerializerView, TestCase):

    pass



class ServiceMetadata(
    ViewSetBase,
    MetadataAttributesFunctional,
    # MetaDataNavigationEntriesFunctional,
    TestCase
):

    # menu_id = 'itim'

    # menu_entry_id = 'service'
    pass
