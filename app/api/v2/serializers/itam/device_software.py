from rest_framework.fields import empty
from rest_framework.reverse import reverse

from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer
from api.v2.serializers.itam.device import BaseSerializer as DeviceBaseSerializer
from api.v2.serializers.itam.software import BaseSerializer as SoftwareBaseSerializer
from api.v2.serializers.itam.software_version import BaseSerializer as SoftwareVeersionBaseSerializer

from itam.models.device import Device, DeviceSoftware

from api.v2.serializers.itam.device import Badge, BadgeField



class BaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )


    url = serializers.HyperlinkedIdentityField(
        view_name="API:_api_v2_device_model-detail", format="html"
    )

    class Meta:

        model = DeviceSoftware

        fields = '__all__'
        # fields = [
        #     'id',
        #     'display_name',
        #     'name',
        #     'url',
        # ]

        # read_only_fields = [
        #     'id',
        #     'display_name',
        #     'name',
        #     # 'url',
        # ]


class ModelSerializer(BaseSerializer):


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, obj):

        return {
            '_self': reverse("API:_api_v2_device_software-detail", request=self._context['view'].request, kwargs={'device_id': self.context['device_id'], 'pk': obj.pk})
        }


    action_badge = BadgeField(default=Badge('a','b','_self'), label='Action')

    # def tester(self):

    #     return {
    #         'a': 'a',
    #         'b':'b'
    #     }

    class Meta:

        model = DeviceSoftware

        fields =  [
             'id',
            'device',
            'software',
            'category',
            'action',
            'action_badge',
            'version',
            'installedversion',
            'installed',
            'organization',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'category',
            'device',
            'installed',
            'installedversion',
            'organization',
            'created',
            'modified',
            '_urls',
        ]


    def __init__(self, instance=None, data=empty, **kwargs):

        super().__init__(instance=instance, data=data, **kwargs)

        if 'device_id' in self._context:

            self.fields.fields['device'].default = self._context['device_id']

            self.fields.fields['device'].initial = self._context['device_id']

            self.fields.fields['organization'].default = Device.objects.get(id=self._context['device_id']).organization.id

            self.fields.fields['organization'].initial = Device.objects.get(id=self._context['device_id']).organization.id


    def is_valid(self, *, raise_exception=False):

        is_valid = super().is_valid(raise_exception=raise_exception)
    
        if 'device_id' in self._context:

            device = Device.objects.get(id=self._context['device_id'])

            self.validated_data['device'] = device
            self.validated_data['organization'] = device.organization

        return is_valid



class ViewSerializer(ModelSerializer):

    organization = OrganizationBaseSerializer(many=False, read_only=True)

    software = SoftwareBaseSerializer(many=False, read_only=True)

    device = DeviceBaseSerializer(many=False, read_only=True)

