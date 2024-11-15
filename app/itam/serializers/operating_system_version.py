from rest_framework.reverse import reverse

from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

from api.serializers import common

from core.serializers.manufacturer import ManufacturerBaseSerializer

from itam.models.operating_system import OperatingSystem, OperatingSystemVersion
from itam.serializers.operating_system import OperatingSystemBaseSerializer



class OperatingSystemVersionBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )


    url = serializers.SerializerMethodField('my_url')

    def my_url(self, item) -> str:

        return reverse(
            "v2:_api_v2_operating_system_version-detail",
            request=self.context['view'].request,
            kwargs={
                'operating_system_id': self._context['view'].kwargs['operating_system_id'],
                'pk': item.pk
            }
        )


    class Meta:

        model = OperatingSystemVersion

        fields = '__all__'
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


class OperatingSystemVersionModelSerializer(
    common.CommonModelSerializer,
    OperatingSystemVersionBaseSerializer
):



    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        return {
            '_self': reverse(
                "v2:_api_v2_operating_system_version-detail",
                request=self._context['view'].request,
                kwargs={
                    'operating_system_id': self._context['view'].kwargs['operating_system_id'],
                    'pk': item.pk
                }
            ),
            'history': reverse(
                "v2:_api_v2_model_history-list",
                request=self._context['view'].request,
                kwargs={
                    'model_class': self.Meta.model._meta.model_name,
                    'model_id': item.pk
                }
            ),
            'notes': reverse(
                "v2:_api_v2_operating_system_notes-list",
                request=self._context['view'].request,
                kwargs={
                    'operating_system_id': item.pk
                }
            ),
            'tickets': 'ToDo'
        }



    class Meta:

        model = OperatingSystemVersion

        fields =  [
             'id',
            'organization',
            'display_name',
            'name',
            'operating_system',
            'model_notes',
            'is_global',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'organization',
            'display_name',
            'operating_system',
            'created',
            'modified',
            '_urls',
        ]



    def is_valid(self, *, raise_exception=False):

        is_valid = super().is_valid(raise_exception=raise_exception)

        if 'view' in self._context:

            if 'operating_system_id' in self._context['view'].kwargs:

                operating_system = OperatingSystem.objects.get(id=self._context['view'].kwargs['operating_system_id'])

                self.validated_data['operating_system'] = operating_system
                self.validated_data['organization'] = operating_system.organization

        return is_valid



class OperatingSystemVersionViewSerializer(OperatingSystemVersionModelSerializer):

    operating_system = OperatingSystemBaseSerializer( many = False, read_only = True )

    organization = OrganizationBaseSerializer( many = False, read_only = True )

