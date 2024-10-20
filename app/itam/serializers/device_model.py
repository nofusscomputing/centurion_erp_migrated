from rest_framework.reverse import reverse

from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

from core.serializers.manufacturer import ManufacturerBaseSerializer

from itam.models.device_models import DeviceModel



class DeviceModelBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )


    url = serializers.HyperlinkedIdentityField(
        view_name="API:_api_v2_device_model-detail", format="html"
    )

    class Meta:

        model = DeviceModel

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


class DeviceModelModelSerializer(DeviceModelBaseSerializer):


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, obj):

        return {
            '_self': reverse("API:_api_v2_device_model-detail", request=self._context['view'].request, kwargs={'pk': obj.pk})
        }

    class Meta:

        model = DeviceModel

        fields =  [
             'id',
            'organization',
            'display_name',
            'manufacturer',
            'name',
            'model_notes',
            'is_global',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'created',
            'modified',
            '_urls',
        ]



class DeviceModelViewSerializer(DeviceModelModelSerializer):

    manufacturer = ManufacturerBaseSerializer( many = False, read_only = True )

    organization = OrganizationBaseSerializer( many = False, read_only = True )
