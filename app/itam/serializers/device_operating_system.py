from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.reverse import reverse

from access.serializers.organization import OrganizationBaseSerializer

from api.serializers import common

from core.fields.badge import Badge, BadgeField

from itam.models.device import Device, DeviceOperatingSystem
from itam.serializers.device import DeviceBaseSerializer
from itam.serializers.operating_system_version import OperatingSystemVersionBaseSerializer



class DeviceOperatingSystemBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )


    url = serializers.SerializerMethodField('my_url')

    def my_url(self, obj) -> str:

        return obj.get_url( request = self._context['request'] )


    class Meta:

        model = DeviceOperatingSystem

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


class DeviceOperatingSystemModelSerializer(
    common.CommonModelSerializer,
    DeviceOperatingSystemBaseSerializer
):


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, obj) -> dict:

        return {
            '_self': obj.get_url( request = self._context['view'].request )
        }


    # action_badge = BadgeField(label='Action')

    # category = SoftwareCategoryBaseSerializer(many=False, read_only=True, source='software.category')


    class Meta:

        model = DeviceOperatingSystem

        fields =  [
             'id',
            'organization',
            'device',
            'operating_system_version',
            'version',
            'installdate',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'created',
            'modified',
            '_urls',
        ]

    # def __init__(self, instance=None, data=empty, **kwargs):

    #     super().__init__(instance=instance, data=data, **kwargs)

    #     if isinstance(self.instance, DeviceOperatingSystem):
                
    #         self.fields.fields['device'].read_only = True

    #         self.fields.fields['software'].read_only = True



    # def is_valid(self, *, raise_exception=False):

    #     is_valid = super().is_valid(raise_exception=raise_exception)

    #     if 'view' in self._context:

    #         if 'device_id' in self._context['view'].kwargs:

    #             device = Device.objects.get(id=self._context['view'].kwargs['device_id'])

    #             self.validated_data['device'] = device
    #             self.validated_data['organization'] = device.organization

    #     return is_valid



class DeviceOperatingSystemViewSerializer(DeviceOperatingSystemModelSerializer):

    device = DeviceBaseSerializer(many=False, read_only=True)

    operating_system_version = OperatingSystemVersionBaseSerializer(many=False, read_only=True)

    organization = OrganizationBaseSerializer(many=False, read_only=True)


