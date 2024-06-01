from django.urls import reverse

from itam.models.device import Device
from rest_framework import serializers




class DeviceSerializer(serializers.ModelSerializer):
    
    url = serializers.HyperlinkedIdentityField(
        view_name="API:_api_device_view", format="html"
    )

    config = serializers.SerializerMethodField('get_device_config')
    
    def get_device_config(self, device):

        request = self.context.get('request')
        return request.build_absolute_uri(reverse('API:_api_device_config', args=[device.slug]))


    class Meta:
        model = Device
        fields = '__all__'

        read_only_fields = [
            'inventorydate',
            'is_global',
            'organization',
        ]

