from django.contrib.auth.models import Permission

from rest_framework import serializers
from rest_framework.reverse import reverse

from app.serializers.content_type import ContentTypeBaseSerializer


class PermissionBaseSerializer(serializers.ModelSerializer):


    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_v2_permission-detail", format="html"
    )

    class Meta:

        model = Permission

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



class PermissionViewSerializer(PermissionBaseSerializer):


    content_type = ContentTypeBaseSerializer()

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        return {
            '_self': reverse("v2:_api_v2_permission-detail", request=self._context['view'].request, kwargs={'pk': item.pk}),
        }


    class Meta:

        model = Permission

        fields =  [
             'id',
            'name',
            'display_name',
            'codename',
            'content_type',
            '_urls',
        ]

        read_only_fields = [
             'id',
            'name',
            'display_name',
            'codename',
            'content_type',
            '_urls',
        ]

