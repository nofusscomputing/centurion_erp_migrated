from django.urls import reverse

from itam.models.device import Device
from rest_framework import serializers




class InventorySerializer(serializers.Serializer):
    """ Serializer for Inventory Upload """


    class DetailsSerializer(serializers.Serializer):

        name = serializers.CharField(
            help_text = 'Host name',
            required = True
        )

        serial_number = serializers.CharField(
            help_text = 'Devices serial number',
            required = True
        )

        uuid = serializers.CharField(
            help_text = 'Device system UUID',
            required = True
        )


    class OperatingSystemSerializer(serializers.Serializer):

        name = serializers.CharField(
            help_text='Name of the operating system installed on the device',
            required = True,
        )

        version_major = serializers.IntegerField(
            help_text='Major semver version number of the OS version',
            required = True,
        )

        version = serializers.CharField(
            help_text='semver version number of the OS',
            required = True
        )


    class SoftwareSerializer(serializers.Serializer):

        name = serializers.CharField(
            help_text='Name of the software',
            required = True
        )

        category = serializers.CharField(
            help_text='Category of the software',
            default = None,
            required = False
        )

        version = serializers.CharField(
            default = None,
            help_text='semver version number of the software',
            required = False
        )


    details = DetailsSerializer()

    os = OperatingSystemSerializer()

    software = SoftwareSerializer(many = True)
