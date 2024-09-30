from rest_framework.reverse import reverse

from rest_framework import serializers

from access.models import Team



class BaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="API:_api_v2_device-detail", format="html"
    )

    class Meta:

        model = Organization

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



class ModelSerializer(BaseSerializer):

    class Meta:

        model = Organization

        fields = '__all__'

        # fields =  [
        #      'id',
        #     'display_name',
        #     'name',
        #     'device_model',
        #     'model_notes',
        #     'is_global',
        #     'serial_number',
        #     'uuid',
        #     'inventorydate',
        #     'created',
        #     'modified',
        #     'organization',
        #     '_urls',
        # ]

        # read_only_fields = [
        #     'id',
        #     'display_name',
        #     'inventorydate',
        #     'created',
        #     'modified',
        #     '_urls',
        # ]


class ViewSerializer(ModelSerializer):

    pass

    # class Meta:

    #     model = Organization

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
    #         'inventorydate',
    #         'created',
    #         'modified',
    #         '_urls',
    #     ]

