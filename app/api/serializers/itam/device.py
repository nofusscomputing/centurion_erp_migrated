from django.urls import reverse

from rest_framework import serializers

from api.serializers.config import ParentGroupSerializer

from config_management.models.groups import ConfigGroups

from itam.models.device import Device



class DeviceConfigGroupsSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="v1:_api_config_group", format="html"
    )

    class Meta:

        model = ConfigGroups

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
        view_name="v1:device-detail", format="html"
    )

    config = serializers.SerializerMethodField('get_device_config')

    groups = DeviceConfigGroupsSerializer(source='configgroups_set', many=True, read_only=True)

    def get_device_config(self, device):

        request = self.context.get('request')
        return request.build_absolute_uri(reverse('v1:_api_device_config', args=[device.slug]))


    class Meta:
        model = Device
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

