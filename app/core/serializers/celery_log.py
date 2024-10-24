import json

from rest_framework.reverse import reverse
from rest_framework import serializers

from django_celery_results.models import TaskResult

from access.serializers.organization import OrganizationBaseSerializer

from app.serializers.user import UserBaseSerializer



class TaskResultBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="API:_api_v2_celery_log-detail", format="html"
    )


    class Meta:

        model = TaskResult

        fields = [
            'id',
            'display_name',
            'url',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'url',
        ]


class TaskResultModelSerializer(TaskResultBaseSerializer):


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        return {
            '_self': reverse("API:_api_v2_celery_log-detail", 
                request=self._context['view'].request,
                kwargs={
                    'pk': item.pk
                }
            ),
        }


    class Meta:

        model = TaskResult

        fields = '__all__'


class TaskResultViewSerializer(TaskResultModelSerializer):

    pass
