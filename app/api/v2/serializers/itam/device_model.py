from rest_framework.reverse import reverse

from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer
from itam.models.device_models import DeviceModel



class BaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )

    # _urls = serializers.SerializerMethodField('get_url')

    # def get_url(self, obj):

    #     return {
    #         '_self': reverse("API:_api_v2_device-detail", request=self._context['view'].request, kwargs={'pk': obj.pk})
    #     }

    url = serializers.HyperlinkedIdentityField(
        view_name="API:_api_v2_device_model-detail", format="html"
    )

    class Meta:

        model = DeviceModel

        # fields = '__all__'
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
            # 'url',
        ]


class ModelSerializer(BaseSerializer):

    pass

    class Meta:

        model = DeviceModel

        fields = '__all__'

    #     fields =  [
    #          'id',
    #         'display_name',
    #         'name',
    #         'device_model',
    #         'model_notes',
    #         'is_global',
    #         'serial_number',
    #         'uuid',
    #         'inventorydate',
    #         'created',
    #         'modified',
    #         'organization',
    #         '_urls',
    #     ]

    #     read_only_fields = [
    #         'id',
    #         'display_name',
    #         'inventorydate',
    #         'created',
    #         'modified',
    #         '_urls',
    #     ]



class ViewSerializer(ModelSerializer):

    organization = OrganizationBaseSerializer(many=False, read_only=True)

