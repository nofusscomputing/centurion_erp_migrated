from rest_framework.reverse import reverse

from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

from settings.models.app_settings import AppSettings



class AppSettingsBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_v2_app_settings-detail", format="html"
    )

    class Meta:

        model = AppSettings

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



class AppSettingsModelSerializer(AppSettingsBaseSerializer):

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        return {
            '_self': reverse("v2:_api_v2_app_settings-detail", request=self._context['view'].request, kwargs={'pk': item.pk}),
        }


    class Meta:

        model = AppSettings

        fields = '__all__'

        # fields =  [
        #     'id',
        #     'organization',
        #     'display_name',
        #     'name',
        #     'template',
        #     'colour',
        #     'cluster',
        #     'devices',
        #     'software',
        #     'model_notes',
        #     'created',
        #     'modified',
        #     '_urls',
        # ]

        # read_only_fields = [
        #     'id',
        #     'display_name',
        #     'created',
        #     'modified',
        #     '_urls',
        # ]


class AppSettingsViewSerializer(AppSettingsModelSerializer):

    global_organization = OrganizationBaseSerializer( many = False, read_only = True )
