from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

from itam.serializers.device import DeviceBaseSerializer

from itim.serializers.cluster import ClusterBaseSerializer
from itim.serializers.port import PortBaseSerializer
from itim.models.services import Service



class ServiceBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="API:_api_v2_service-detail", format="html"
    )

    class Meta:

        model = Service

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


class ServiceModelSerializer(ServiceBaseSerializer):

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        return {
            '_self': reverse("API:_api_v2_service-detail", request=self._context['view'].request, kwargs={'pk': item.pk}),
            'history': reverse(
                "API:_api_v2_model_history-list",
                request=self._context['view'].request,
                kwargs={
                    'model_class': self.Meta.model._meta.model_name,
                    'model_id': item.pk
                }
            ),
            'notes': reverse("API:_api_v2_service_notes-list", request=self._context['view'].request, kwargs={'service_id': item.pk}),
            'tickets': 'ToDo'
        }


    rendered_config = serializers.JSONField(source='config_variables')


    class Meta:

        model = Service

        fields =  [
             'id',
            'organization',
            'display_name',
            'name',
            'model_notes',
            'is_template',
            'template',
            'device',
            'cluster',
            'config',
            'rendered_config',
            'config_key_variable',
            'port',
            'dependent_service',
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



class ServiceViewSerializer(ServiceModelSerializer):

    cluster = ClusterBaseSerializer( many = False, read_only = True )

    device = DeviceBaseSerializer( many = False, read_only = True )

    dependent_service = ServiceBaseSerializer( many = True, read_only = True )

    organization = OrganizationBaseSerializer( many = False, read_only = True )

    port = PortBaseSerializer( many = True, read_only = True )

    template = ServiceBaseSerializer( many = False, read_only = True )
