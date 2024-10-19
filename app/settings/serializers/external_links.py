from rest_framework.reverse import reverse

from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

from settings.models.external_link import ExternalLink



class ExternalLinkBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="API:_api_v2_external_link-detail", format="html"
    )

    class Meta:

        model = ExternalLink

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



class ExternalLinkModelSerializer(ExternalLinkBaseSerializer):

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        return {
            '_self': reverse("API:_api_v2_external_link-detail", request=self._context['view'].request, kwargs={'pk': item.pk}),
            'history': reverse(
                "API:_api_v2_model_history-list",
                request=self._context['view'].request,
                kwargs={
                    'model_class': self.Meta.model._meta.model_name,
                    'model_id': item.pk
                }
            ),
            'notes': reverse("API:_api_v2_device_notes-list", request=self._context['view'].request, kwargs={'device_id': item.pk}),
        }


    class Meta:

        model = ExternalLink

        fields = '__all__'

        fields =  [
            'id',
            'organization',
            'display_name',
            'name',
            'template',
            'colour',
            'cluster',
            'devices',
            'software',
            'model_notes',
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


class ExternalLinkViewSerializer(ExternalLinkModelSerializer):

    organization = OrganizationBaseSerializer( many = False, read_only = True )
