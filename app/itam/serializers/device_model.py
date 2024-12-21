from rest_framework.reverse import reverse

from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

from api.serializers import common

from core.serializers.manufacturer import ManufacturerBaseSerializer

from itam.models.device_models import DeviceModel



class DeviceModelBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )


    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_v2_device_model-detail", format="html"
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


class DeviceModelModelSerializer(
    common.CommonModelSerializer,
    DeviceModelBaseSerializer
):


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, obj) -> dict:

        return {
            '_self': obj.get_url( request = self._context['view'].request ),
            'knowledge_base': reverse(
                "v2:_api_v2_model_kb-list",
                request=self._context['view'].request,
                kwargs={
                    'model': self.Meta.model._meta.model_name,
                    'model_pk': item.pk
                }
            ),
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

