from rest_framework.reverse import reverse
from rest_framework import serializers

from django.contrib.auth.models import User

from access.models import Organization



class UserBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )

    # url = serializers.HyperlinkedIdentityField(
    #     view_name="API:_api_v2_organization-detail", format="html"
    # )

    class Meta:

        model = User

        fields = '__all__'

        fields = [
            'id',
            'display_name',
            'first_name',
            'last_name',
            'username',
            'is_active',
            # 'url',
        ]

        # read_only_fields = [
        #     'id',
        #     'display_name',
        #     'name',
        #     'url',
        # ]



class UserModelSerializer(UserBaseSerializer):

    class Meta:

        model = User

        fields = '__all__'

        fields =  [
             'id',
            'display_name',
            'name',
            'device_model',
            'model_notes',
            'is_global',
            'serial_number',
            'uuid',
            'inventorydate',
            'created',
            'modified',
            'organization',
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


class UserViewSerializer(UserModelSerializer):

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

