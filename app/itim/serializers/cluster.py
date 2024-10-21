from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

from itam.serializers.device import DeviceBaseSerializer

from itim.serializers.cluster_type import ClusterTypeBaseSerializer
from itim.models.clusters import Cluster



class ClusterBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="API:_api_v2_cluster-detail", format="html"
    )

    class Meta:

        model = Cluster

        fields = [
            'id',
            'display_name',
            'name',
            'url',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'name',
            'url',
        ]


class ClusterModelSerializer(ClusterBaseSerializer):

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        return {
            '_self': reverse("API:_api_v2_cluster-detail", request=self._context['view'].request, kwargs={'pk': item.pk}),
            'history': reverse(
                "API:_api_v2_model_history-list",
                request=self._context['view'].request,
                kwargs={
                    'model_class': self.Meta.model._meta.model_name,
                    'model_id': item.pk
                }
            ),
            'notes': reverse("API:_api_v2_cluster_notes-list", request=self._context['view'].request, kwargs={'cluster_id': item.pk}),
            'tickets': 'ToDo'
        }


    rendered_config = serializers.JSONField()


    class Meta:

        model = Cluster

        fields =  [
             'id',
            'organization',
            'display_name',
            'name',
            'model_notes',
            'parent_cluster',
            'cluster_type',
            'config',
            'rendered_config',
            'nodes',
            'devices',
            'is_global',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'rendered_config',
            'created',
            'modified',
            '_urls',
        ]



class ClusterViewSerializer(ClusterModelSerializer):

    cluster_type = ClusterTypeBaseSerializer( many = False, read_only = True )

    devices = DeviceBaseSerializer( many = True, read_only = True )

    nodes = DeviceBaseSerializer( many = True, read_only = True )

    organization = OrganizationBaseSerializer( many = False, read_only = True )

    parent_cluster = ClusterBaseSerializer( many = False, read_only = True )
