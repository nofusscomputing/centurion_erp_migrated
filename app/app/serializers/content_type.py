from django.contrib.auth.models import ContentType

from rest_framework import serializers
from rest_framework.reverse import reverse



class ContentTypeBaseSerializer(serializers.ModelSerializer):


    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_v2_content_type-detail", format="html"
    )

    class Meta:

        model = ContentType

        fields = '__all__'

        fields = [
            'id',
            'display_name',
            'url'
        ]

        read_only_fields = [
            'id',
            'display_name',
            'url'
        ]



class ContentTypeViewSerializer(ContentTypeBaseSerializer):


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        return {
            '_self': reverse("v2:_api_v2_content_type-detail", request=self._context['view'].request, kwargs={'pk': item.pk}),
        }


    class Meta:

        model = ContentType

        fields =  [
             'id',
            'app_label',
            'model',
            '_urls',
        ]

        read_only_fields = [
             'id',
            'app_label',
            'model',
            '_urls',
        ]