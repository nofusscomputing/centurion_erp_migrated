from rest_framework.reverse import reverse
from rest_framework import serializers

from app.serializers.user import UserBaseSerializer

from core.models.history import History



class HistoryBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )

    url = serializers.SerializerMethodField('get_my_url')

    def get_my_url(self, item):

        return reverse("API:_api_v2_model_history-detail", 
                request=self._context['view'].request,
                kwargs={
                    'model_class': self._kwargs['context']['view'].kwargs['model_class'],
                    'model_id': self._kwargs['context']['view'].kwargs['model_id'],
                    'pk': item.pk
                }
            )


    class Meta:

        model = History

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


class HistoryModelSerializer(HistoryBaseSerializer):


    after = serializers.JSONField(read_only=True)

    before = serializers.JSONField(read_only=True)

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        return {
            '_self': reverse("API:_api_v2_model_history-detail", 
                request=self._context['view'].request,
                kwargs={
                    'model_class': self._kwargs['context']['view'].kwargs['model_class'],
                    'model_id': self._kwargs['context']['view'].kwargs['model_id'],
                    'pk': item.pk
                }
            ),
        }


    class Meta:

        model = History

        fields =  [
             'id',
            'display_name',
            'before',
            'after',
            'action',
            'user',
            'item_pk',
            'item_class',
            'item_parent_pk',
            'item_parent_class',
            'created',
            '_urls',
        ]

        read_only_fields = [
             'id',
            'display_name',
            'created',
            '_urls',
        ]



class HistoryViewSerializer(HistoryModelSerializer):

    user = UserBaseSerializer( read_only = True )

    pass
