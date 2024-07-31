from rest_framework import serializers
from rest_framework.reverse import reverse

from config_management.models.groups import ConfigGroups



class ParentGroupSerializer(serializers.ModelSerializer):

    url = serializers.SerializerMethodField('get_url')


    class Meta:
        model = ConfigGroups
        fields = [
            'id',
            'name',
            'url',
        ]
        read_only_fields = [
            'id',
            'name',
            'url',
        ]


    def get_url(self, obj):

        request = self.context.get('request')

        return request.build_absolute_uri(reverse("API:_api_config_group", args=[obj.pk]))



class ConfigGroupsSerializerBase(serializers.ModelSerializer):

    parent = ParentGroupSerializer(read_only=True)
    url = serializers.SerializerMethodField('get_url')


    class Meta:
        model = ConfigGroups
        fields = [
            'id',
            'parent',
            'name',
            'config',
            'url',
        ]
        read_only_fields = [
            'id',
            'name',
            'config',
            'url',
        ]


    def get_url(self, obj):

        request = self.context.get('request')

        return request.build_absolute_uri(reverse("API:_api_config_group", args=[obj.pk]))



class ConfigGroupsSerializer(ConfigGroupsSerializerBase):


    class Meta:
        model = ConfigGroups
        depth = 1
        fields = [
            'id',
            'parent',
            'name',
            'config',
            'url',
        ]
        read_only_fields = [
            'id',
            'parent',
            'name',
            'config',
            'url',
        ]

