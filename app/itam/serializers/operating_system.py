from rest_framework.reverse import reverse

from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer
from itam.models.operating_system import OperatingSystem



class OperatingSystemBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )

    class Meta:

        model = OperatingSystem

        fields = '__all__'
        fields = [
            'id',
            'display_name',
            'name',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'name',
        ]
