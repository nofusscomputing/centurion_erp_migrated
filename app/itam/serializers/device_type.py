from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

from api.serializers import common

from itam.models.device import DeviceType



class DeviceTypeBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_v2_device_type-detail", format="html"
    )

    class Meta:

        model = DeviceType

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


class DeviceTypeModelSerializer(
    common.CommonModelSerializer,
    DeviceTypeBaseSerializer
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

        model = DeviceType

        fields =  [
             'id',
            'display_name',
            'organization',
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
            'inventorydate',
            'created',
            'modified',
            '_urls',
        ]



class DeviceTypeViewSerializer(DeviceTypeModelSerializer):

    organization = OrganizationBaseSerializer(many=False, read_only=True)

