from rest_framework.reverse import reverse

from rest_framework import serializers

from settings.models.external_link import ExternalLink

# from app.serializers.user import UserBaseSerializer



class ExternalLinkBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="API:_api_v2_organization-detail", format="html"
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

    # _urls = serializers.SerializerMethodField('get_url')

    # def get_url(self, item):

    #     return {
    #         '_self': reverse("API:_api_v2_organization-detail", request=self._context['view'].request, kwargs={'pk': item.pk}),
    #         'teams': 'ToDo',
    #     }


    class Meta:

        model = ExternalLink

        fields = '__all__'

        # fields =  [
        #      'id',
        #     'display_name',
        #     'name',
        #     'model_notes',
        #     'manager',
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


class ExternalLinkViewSerializer(ExternalLinkModelSerializer):
    pass

    # manager = UserBaseSerializer(many=False, read_only = True)
