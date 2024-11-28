from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.reverse import reverse

from access.serializers.organization import OrganizationBaseSerializer

from api.serializers import common

from core import exceptions as centurion_exception
from core.fields.badge import Badge, BadgeField

from itam.models.device import Device, DeviceSoftware
from itam.serializers.device import DeviceBaseSerializer
from itam.serializers.software import Software, SoftwareBaseSerializer
from itam.serializers.software_category import SoftwareCategoryBaseSerializer
from itam.serializers.software_version import SoftwareVersionBaseSerializer



class DeviceSoftwareBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )


    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_v2_device_software-detail", format="html"
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


class DeviceSoftwareModelSerializer(
    common.CommonModelSerializer,
    DeviceSoftwareBaseSerializer
):


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, obj) -> dict:

         if 'view' in self._context:

            if 'software_id' in self._context['view'].kwargs:

                return {
                    '_self': reverse("v2:_api_v2_software_installs-detail", request = self._context['view'].request, kwargs = {
                        'software_id': obj.software.pk,
                        'pk': obj.pk
                    } )
                }

            elif 'device_id' in self._context['view'].kwargs:

                return {
                    '_self': obj.get_url( request = self._context['view'].request )
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
            'category',
            'device',
            'installed',
            'installedversion',
            'organization',
            'created',
            'modified',
            '_urls',
        ]


    def validate(self, data):


        if 'view' in self._context:

            if 'device_id' in self._context['view'].kwargs:

                device = Device.objects.get(id=self._context['view'].kwargs['device_id'])

                data['device'] = device
                data['organization'] = device.organization

            if 'software_id' in self._context['view'].kwargs:

                software = Software.objects.get(id=int(self._context['view'].kwargs['software_id']))

                data['software'] = software

                if 'device' in data:

                    data['organization'] = data['device'].organization


        if(
            not data.get('device')
            and not getattr(self.instance, 'device', None)
        ):

            raise centurion_exception.ValidationError(
                detail = {
                    'device': 'This field is required'
                },
                code =  'required'
            )


        if(
            not data.get('software')
            and not getattr(self.instance, 'software', None)
        ):

            raise centurion_exception.ValidationError(
                detail = {
                    'software': 'This field is required',
                },
                code =  'required'
            )

        return data




class SoftwareInstallsModelSerializer(
    DeviceSoftwareModelSerializer
):


    class Meta( DeviceSoftwareModelSerializer.Meta ):

        read_only_fields = [
            'id',
            'category',
            'software',
            'installed',
            'installedversion',
            'organization',
            'created',
            'modified',
            '_urls',

        ]



class DeviceSoftwareViewSerializer(DeviceSoftwareModelSerializer):

    device = DeviceBaseSerializer(many=False, read_only=True)

    installedversion = SoftwareVersionBaseSerializer(many=False, read_only=True)

    organization = OrganizationBaseSerializer(many=False, read_only=True)

    software = SoftwareBaseSerializer(many=False, read_only=True)

    version = SoftwareVersionBaseSerializer(many=False, read_only=True)

