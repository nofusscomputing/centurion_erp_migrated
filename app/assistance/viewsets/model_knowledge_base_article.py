import importlib

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from api.viewsets.common import ModelViewSet

from assistance.serializers.model_knowledge_base_article import (
    all_models,
    ModelKnowledgeBaseArticle,
    ModelKnowledgeBaseArticleModelSerializer,
    ModelKnowledgeBaseArticleViewSerializer,
)

from django.apps import apps



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a knowledge base article',
        description='',
        responses = {
            201: OpenApiResponse(description='Created', response=ModelKnowledgeBaseArticleViewSerializer),
            403: OpenApiResponse(description='User is missing add permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a knowledge base article',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all knowledge base articles',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ModelKnowledgeBaseArticleViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single knowledge base article',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ModelKnowledgeBaseArticleViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a knowledge base article',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=ModelKnowledgeBaseArticleViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):

    filterset_fields = [
        'organization',
        'article',
    ]

    search_fields = [
        'article.title',
    ]

    model = ModelKnowledgeBaseArticle

    documentation: str = ''

    view_description = 'Model Knowledge Base Article(s)'



    def get_back_url(self) -> str:

        if(
            getattr(self, '_back_url', None) is None
        ):

            model_value: str = ''

            for value, display_name in all_models():

                value_model = str(value).split('.')[1]

                if value_model == self.kwargs['model']:

                    model_value = value


            for model in apps.get_models():

                if(
                    str(model._meta.app_label) + '.' + str(model._meta.model_name)
                    ==
                    model_value
                ):

                    app = importlib.import_module( model.__module__ )

                    model_class = getattr(app, model.__name__)

                    item = model_class.objects.get(pk = int(self.kwargs['model_pk']))

                    if item:

                        self._back_url = str(
                            item.get_url( self.request )
                        )


        return self._back_url


    def get_queryset(self):

        queryset = super().get_queryset()

        for value, display_name in all_models():

            value_model = str(value).split('.')[1]

            if value_model == self.kwargs['model']:

                queryset = queryset.filter(
                    model = value,
                    model_pk = int(self.kwargs['model_pk'])
                )

                break

        return queryset


    def get_serializer_class(self):

        all_models = apps.get_models()
        
        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ViewSerializer']


        return globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ModelSerializer']

