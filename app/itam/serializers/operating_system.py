from rest_framework.reverse import reverse

from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

from core.serializers.manufacturer import ManufacturerBaseSerializer

from itam.models.operating_system import OperatingSystem



class OperatingSystemBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_v2_operating_system-detail", format="html"
    )

    class Meta:

        model = OperatingSystem

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


class OperatingSystemModelSerializer(OperatingSystemBaseSerializer):



    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        request = None

        if 'view' in self._context:

            if hasattr(self._context['view'], 'request'):

                request = self._context['view'].request

        return {
            '_self': item.get_url( request = request ),
            'history': reverse(
                "v2:_api_v2_model_history-list",
                request=self._context['view'].request,
                kwargs={
                    'model_class': self.Meta.model._meta.model_name,
                    'model_id': item.pk
                }
            ),
            'notes': reverse("v2:_api_v2_operating_system_notes-list", request=self._context['view'].request, kwargs={'operating_system_id': item.pk}),
            'tickets': reverse(
                "v2:_api_v2_item_tickets-list",
                request=self._context['view'].request,
                kwargs={
                    'item_class': 'operating_system',
                    'item_id': item.pk
                    }
            ),
            'version': reverse("v2:_api_v2_operating_system_version-list", request=self._context['view'].request, kwargs={'operating_system_id': item.pk}),
        }



    class Meta:

        model = OperatingSystem

        fields =  [
             'id',
            'organization',
            'display_name',
            'publisher',
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
            'created',
            'modified',
            '_urls',
        ]



class OperatingSystemViewSerializer(OperatingSystemModelSerializer):

    organization = OrganizationBaseSerializer( many = False, read_only = True )

    publisher = ManufacturerBaseSerializer( many = False, read_only = True )

