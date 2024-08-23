from django.urls import reverse

from rest_framework import serializers

from api.serializers.config import ParentGroupSerializer

from config_management.models.groups import ConfigGroupHosts

from itam.models.device import Device



class DeviceConfigGroupsSerializer(serializers.ModelSerializer):

    name = serializers.CharField(source='group.name', read_only=True)

    url = serializers.HyperlinkedIdentityField(
        view_name="API:_api_config_group", format="html"
    )

    class Meta:

        model = ConfigGroupHosts

        fields = [
            'id',
            'name',
            'url',

        ]
        read_only_fields = [
            'id',
            'name',
            'url',
        ]


class DeviceSerializer(serializers.ModelSerializer):
    
    url = serializers.HyperlinkedIdentityField(
        view_name="API:device-detail", format="html"
    )

    config = serializers.SerializerMethodField('get_device_config')

    groups = DeviceConfigGroupsSerializer(source='configgrouphosts_set', many=True, read_only=True)

    def get_device_config(self, device):

        request = self.context.get('request')
        return request.build_absolute_uri(reverse('API:_api_device_config', args=[device.slug]))


    class Meta:
        model = Device
        depth = 1
        fields =  [
            'id',
            'is_global',
            'name',
            'config',
            'serial_number',
            'uuid',
            'inventorydate',
            'created',
            'modified',
            'groups',
            'organization',
            'url',
        ]

        read_only_fields = [
            'id',
            'config',
            'inventorydate',
            'created',
            'modified',
            'groups',
            'url',
        ]

