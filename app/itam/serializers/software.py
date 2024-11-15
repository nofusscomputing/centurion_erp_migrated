from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

from api.serializers import common

from core.serializers.manufacturer import ManufacturerBaseSerializer

from itam.models.software import Software
from itam.serializers.software_category import SoftwareCategoryBaseSerializer



class SoftwareBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_v2_software-detail", format="html"
    )

    class Meta:

        model = Software

        fields = [
            'id',
            'display_name',
            'name',
            'url'
        ]

        read_only_fields = [
            'id',
            'display_name',
            'name',
            'url'
        ]


class SoftwareModelSerializer(
    common.CommonModelSerializer,
    SoftwareBaseSerializer
):


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        request = None

        if 'view' in self._context:

            if hasattr(self._context['view'], 'request'):

                request = self._context['view'].request

        return {
            '_self': item.get_url( request = request ),
            'external_links': reverse("v2:_api_v2_external_link-list", request=self._context['view'].request) + '?software=true',
            'history': reverse(
                "v2:_api_v2_model_history-list",
                request=self._context['view'].request,
                kwargs={
                    'model_class': self.Meta.model._meta.model_name,
                    'model_id': item.pk
                }
            ),
            'notes': reverse("v2:_api_v2_software_notes-list", request=self._context['view'].request, kwargs={'software_id': item.pk}),
            'publisher': reverse("v2:_api_v2_manufacturer-list", request=self._context['view'].request),
            'services': 'ToDo',
            'version': reverse(
                "v2:_api_v2_software_version-list",
                request=self._context['view'].request,
                kwargs={
                    'software_id': item.pk
                }
            ),
            'tickets': reverse(
                "v2:_api_v2_item_tickets-list",
                request=self._context['view'].request,
                kwargs={
                    'item_class': 'software',
                    'item_id': item.pk
                    }
            )
        }


    def get_rendered_config(self, item) -> dict:

        return item.get_configuration(0)


    class Meta:

        model = Software

        fields = '__all__'

        fields =  [
             'id',
            'organization',
            'publisher',
            'display_name',
            'name',
            'category',
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



class SoftwareViewSerializer(SoftwareModelSerializer):

    category = SoftwareCategoryBaseSerializer( many = False, read_only = True )

    organization = OrganizationBaseSerializer( many = False, read_only = True )

    publisher = ManufacturerBaseSerializer( many = False, read_only = True )
