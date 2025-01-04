from django.db.models import Q
from django.urls import reverse

from rest_framework import serializers

from core import exceptions as centurion_exceptions

from itam.models.device import Device




class InventorySerializer(serializers.Serializer):
    """ Serializer for Inventory Upload """


    class DetailsSerializer(serializers.Serializer):

        name = serializers.CharField(
            help_text = 'Host name',
            required = True
        )

        serial_number = serializers.CharField(
            default = None,
            help_text = 'Devices serial number',
            required = False
        )

        uuid = serializers.CharField(
            default = None,
            help_text = 'Device system UUID',
            required = False
        )


        def validate(self, data):

            if(
                data['serial_number'] is None
                and data['uuid'] is None
            ):

                raise centurion_exceptions.ValidationError(
                    detail = 'Serial Number and/or UUID is required',
                    code = 'no_serial_or_uuid'
                )


            obj = Device.objects.filter(
                Q(
                    name=str(data['name']).lower(),
                    serial_number = str(data['serial_number']).lower()
                )
                  |
                Q(
                    name = str(data['name']).lower(),
                    uuid = str(data['uuid']).lower()
                )
                    |
                Q(
                    serial_number = str(data['serial_number']).lower()
                )
                  |
                Q(
                    uuid = str(data['uuid']).lower()
                )
            )

            if len(obj) > 1:

                raise centurion_exceptions.ValidationError(
                    detail = {
                        'detail': 'Object is not unique. Confirm that uuid and/or serial number is unique'
                    },
                    code = 'not_unique'
                )

            elif len(obj) == 1:

                obj = obj[0]

                if obj.name == str(data['name']).lower():

                    if(
                        obj.serial_number != str(data['serial_number']).lower()
                        and obj.uuid != str(data['uuid']).lower()
                    ):

                        raise centurion_exceptions.ValidationError(
                            detail = {
                                'detail': 'Device exists, however the serial number and/or UUID dont match'
                            },
                            code = 'not_unique'
                        )



            return data


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

    os = OperatingSystemSerializer( required = False )

    software = SoftwareSerializer( many = True, required = False )
