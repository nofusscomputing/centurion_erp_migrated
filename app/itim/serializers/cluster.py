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
        view_name="v2:_api_v2_cluster-detail",
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

        request = None

        if 'view' in self._context:

            if hasattr(self._context['view'], 'request'):

                request = self._context['view'].request

        return {
            '_self': item.get_url( request = request ),
            'history': reverse(
                "v2:_api_v2_model_history-list",
                request=self._context['view'].request,
                kwargs={
                    'model_class': self.Meta.model._meta.model_name,
                    'model_id': item.pk
                }
            ),
            'notes': reverse("v2:_api_v2_cluster_notes-list", request=self._context['view'].request, kwargs={'cluster_id': item.pk}),
            'tickets': reverse(
                "v2:_api_v2_item_tickets-list",
                request=self._context['view'].request,
                kwargs={
                    'item_class': 'cluster',
                    'item_id': item.pk
                    }
            )
        }


    rendered_config = serializers.JSONField( read_only = True)
    
    resources = serializers.CharField(
        label = 'Available Resources',
        read_only = True,
        initial = 'xx/yy CPU, xx/yy RAM, xx/yy Storage',
        default = 'xx/yy CPU, xx/yy RAM, xx/yy Storage',
    )


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
            'resources',
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
            'resources',
            'created',
            'modified',
            '_urls',
        ]


    def is_valid(self, *, raise_exception=False):

        is_valid = super().is_valid(raise_exception=raise_exception)


        if 'parent_cluster' in self.validated_data:

            if hasattr(self.instance, 'id') and self.validated_data['parent_cluster']:

                if self.validated_data['parent_cluster'].id == self.instance.id:

                    is_valid = False

                    raise serializers.ValidationError(
                        detail = {
                            "parent_cluster": "Cluster can't have itself as its parent cluster"
                        },
                        code = 'parent_not_self'
                    )

        return is_valid



class ClusterViewSerializer(ClusterModelSerializer):

    cluster_type = ClusterTypeBaseSerializer( many = False, read_only = True )

    devices = DeviceBaseSerializer( many = True, read_only = True )

    nodes = DeviceBaseSerializer( many = True, read_only = True )

    organization = OrganizationBaseSerializer( many = False, read_only = True )

    parent_cluster = ClusterBaseSerializer( many = False, read_only = True )
