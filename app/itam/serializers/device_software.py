from rest_framework.fields import empty
from rest_framework.reverse import reverse

from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

from core.fields.badge import Badge, BadgeField

from itam.models.device import Device, DeviceSoftware
from itam.serializers.device import DeviceBaseSerializer
from itam.serializers.software import SoftwareBaseSerializer
from itam.serializers.software_category import SoftwareCategoryBaseSerializer
from itam.serializers.software_version import SoftwareVersionBaseSerializer



class DeviceSoftwareBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )


    url = serializers.HyperlinkedIdentityField(
        view_name="API:_api_v2_device_software-detail", format="html"
    )


    class Meta:

        model = DeviceSoftware

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


class DeviceSoftwareModelSerializer(DeviceSoftwareBaseSerializer):


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, obj):

        return {
            '_self': reverse(
                "API:_api_v2_device_software-detail",
                request=self._context['view'].request,
                kwargs={
                    'device_id': self._context['view'].kwargs['device_id'],
                    'pk': obj.pk
                }
            )
        }


    action_badge = BadgeField(label='Action')

    category = SoftwareCategoryBaseSerializer(many=False, read_only=True, source='software.category')


    class Meta:

        model = DeviceSoftware

        fields =  [
             'id',
            'organization',
            'device',
            'software',
            'category',
            'action',
            'action_badge',
            'version',
            'installedversion',
            'installed',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'software',
            'category',
            'device',
            'installed',
            'installedversion',
            'organization',
            'created',
            'modified',
            '_urls',
        ]


    def is_valid(self, *, raise_exception=False):

        is_valid = super().is_valid(raise_exception=raise_exception)

        if 'view' in self._context:

            if 'device_id' in self._context['view'].kwargs:

                device = Device.objects.get(id=self._context['view'].kwargs['device_id'])

                self.validated_data['device'] = device
                self.validated_data['organization'] = device.organization

        return is_valid



class DeviceSoftwareViewSerializer(DeviceSoftwareModelSerializer):

    device = DeviceBaseSerializer(many=False, read_only=True)

    installedversion = SoftwareVersionBaseSerializer(many=False, read_only=True)

    organization = OrganizationBaseSerializer(many=False, read_only=True)

    software = SoftwareBaseSerializer(many=False, read_only=True)

    version = SoftwareVersionBaseSerializer(many=False, read_only=True)

