import json

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

from api.viewsets.common import ModelViewSet

from core.fields.icon import Icon, IconField

from itam.models.device import Device
from itam.serializers.device_model import DeviceModelBaseSerializer
from itam.serializers.device_type import DeviceTypeBaseSerializer




class DeviceBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_v2_device-detail", format="html"
    )

    class Meta:

        model = Device

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

class DeviceModelSerializer(DeviceBaseSerializer):

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        request = None

        if 'view' in self._context:

            if hasattr(self._context['view'], 'request'):

                request = self._context['view'].request

        return {
            '_self': item.get_url( request = request ),
            'device_model': reverse("v2:_api_v2_device_model-list", request=self._context['view'].request),
            'device_type': reverse("v2:_api_v2_device_type-list", request=self._context['view'].request),
            'external_links': reverse("v2:_api_v2_external_link-list", request=self._context['view'].request) + '?devices=true',
            'history': reverse(
                "v2:_api_v2_model_history-list",
                request=self._context['view'].request,
                kwargs={
                    'model_class': self.Meta.model._meta.model_name,
                    'model_id': item.pk
                }
            ),
            'notes': reverse("v2:_api_v2_device_notes-list", request=self._context['view'].request, kwargs={'device_id': item.pk}),
            'service': reverse("v2:_api_v2_service_device-list", request=self._context['view'].request, kwargs={'device_id': item.pk}),
            'software': reverse("v2:_api_v2_device_software-list", request=self._context['view'].request, kwargs={'device_id': item.pk}),
        }


    context = serializers.SerializerMethodField('get_cont')

    def get_cont(self, item) -> dict:

        from django.core.serializers import serialize

        device = json.loads(serialize('json', [item]))

        fields = device[0]['fields']

        fields.update({'id': device[0]['pk']})

        context: dict = {}

        return context


    rendered_config = serializers.JSONField(source='get_configuration', read_only=True)

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

    device_model = DeviceModelBaseSerializer( many = False, read_only = True )

    device_type = DeviceTypeBaseSerializer( many = False, read_only = True )

    organization = OrganizationBaseSerializer( many = False, read_only = True )
