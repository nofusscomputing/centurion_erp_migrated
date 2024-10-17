from rest_framework import serializers
from rest_framework.reverse import reverse

from access.serializers.organization import OrganizationBaseSerializer

from itam.models.software import Software



class SoftwareBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )

    class Meta:

        model = Software

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
