import json

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

from api.viewsets.common import ModelViewSet

from core.fields.icon import Icon, IconField

from access.serializers.organization import OrganizationBaseSerializer

from itam.models.device import Device



class DeviceBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )

    class Meta:

        model = Device

        fields = [
            'id',
            'display_name',
            'name',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'name',
        ]

class DeviceModelSerializer(DeviceBaseSerializer):

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        return {
            '_self': reverse("API:_api_v2_device-detail", request=self._context['view'].request, kwargs={'pk': item.pk}),
            'history': reverse(
                "API:_api_v2_model_history-list",
                request=self._context['view'].request,
                kwargs={
                    'model_class': self.Meta.model._meta.model_name,
                    'model_id': item.pk
                }
            ),
            'notes': reverse("API:_api_v2_device_notes-list", request=self._context['view'].request, kwargs={'device_id': item.pk}),
        }


    rendered_config = serializers.JSONField(source='get_configuration', read_only=True)

    context = serializers.SerializerMethodField('get_cont')


    def get_cont(self, item) -> dict:

        from django.core.serializers import serialize

        device = json.loads(serialize('json', [item]))

        fields = device[0]['fields']

        fields.update({'id': device[0]['pk']})

        context: dict = {}

        return context
    

    def get_rendered_config(self, item):

        return item.get_configuration(0)


    status_icon = IconField(read_only = True, label='')

    class Meta:

        model = Device

        fields =  [
             'id',
             'status_icon',
            'display_name',
            'name',
            'device_type',
            'model_notes',
            'serial_number',
            'uuid',
            'is_global',
            'is_virtual',
            'device_model',
            'config',
            'rendered_config',
            'inventorydate',
            'context',
            'created',
            'modified',
            'organization',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'context',
            'display_name',
            'inventorydate',
            'rendered_config',
            'created',
            'modified',
            '_urls',
        ]



class DeviceViewSerializer(DeviceModelSerializer):

    organization = OrganizationBaseSerializer(many=False, read_only=True)
