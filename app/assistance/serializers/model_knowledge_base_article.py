from django.apps import apps

from rest_framework import serializers
from rest_framework.reverse import reverse

from access.serializers.organization import OrganizationBaseSerializer

from api.serializers import common

from assistance.models.model_knowledge_base_article import all_models, ModelKnowledgeBaseArticle
from assistance.serializers.knowledge_base import KnowledgeBaseBaseSerializer
from assistance.serializers.knowledge_base_category import KnowledgeBaseCategoryBaseSerializer

from core import exceptions as centurion_exceptions



class ModelKnowledgeBaseArticleBaseSerializer(serializers.ModelSerializer):


    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item.article.title )

    url = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> str:

        return item.article.get_url( request = self.context['view'].request )


    class Meta:

        model = ModelKnowledgeBaseArticle

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



class ModelKnowledgeBaseArticleModelSerializer(
    common.CommonModelSerializer,
   ModelKnowledgeBaseArticleBaseSerializer
):


    category = serializers.PrimaryKeyRelatedField(source = 'article.category', read_only = True)

    class Meta:

        model = ModelKnowledgeBaseArticle

        fields =  [
            'id',
            'organization',
            'article',
            'category',
            'created',
            'modified',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'created',
            'modified',
        ]


    def is_valid(self, *, raise_exception=False):

        is_valid: bool = False

        is_valid = super().is_valid(raise_exception=raise_exception)


        if 'view' in self._context:

            if(
                not self._kwargs['context']['view'].kwargs.get('model', None)
                or not self._kwargs['context']['view'].kwargs.get('model_pk', None)
            ):

                raise centurion_exceptions.ValidationError(
                    detail = 'Both model and model_pk must be supplied',
                    code = 'model_details_required'
                )


            if self._context['view'].action == 'create':

                for value, display_name in all_models():

                    value_model = str(value).split('.')[1]

                    if value_model == self._kwargs['context']['view'].kwargs['model']:

                        self.validated_data['model'] = value

                        break


                self.validated_data['model_pk'] = int(self._kwargs['context']['view'].kwargs['model_pk'])


            if not self.validated_data.get('model', None):

                 raise centurion_exceptions.ValidationError(
                    detail = {
                        'model': 'This field is required'
                    },
                    code = 'required'
                )

            if not self.validated_data.get('model_pk', None):

                 raise centurion_exceptions.ValidationError(
                    detail = {
                        'model_pk': 'This field is required'
                    },
                    code = 'required'
                )

        return is_valid



class ModelKnowledgeBaseArticleViewSerializer(ModelKnowledgeBaseArticleModelSerializer):

    article = KnowledgeBaseBaseSerializer( read_only = True )

    category = KnowledgeBaseCategoryBaseSerializer(source = 'article.category', read_only = True )

    organization = OrganizationBaseSerializer( many=False, read_only=True )
