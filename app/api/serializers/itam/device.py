from rest_framework import serializers
from itam.models.device import Device




class DeviceSerializer(serializers.ModelSerializer):
    
    url = serializers.HyperlinkedIdentityField(
        view_name="_api_device_view", format="html"
    )

    config = serializers.SerializerMethodField('get_device_config')

    def get_device_config(self, device):

        return device.get_configuration(device.id)



    class Meta:
        model = Device
        fields = '__all__'
