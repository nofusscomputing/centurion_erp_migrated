from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from api.viewsets.common import ModelViewSet

from assistance.serializers.knowledge_base_category import (
    KnowledgeBaseCategory,
    KnowledgeBaseCategoryModelSerializer,
    KnowledgeBaseCategoryViewSerializer
)



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a knowledge base article',
        description='',
        responses = {
            # 200: OpenApiResponse(description='Allready exists', response=KnowledgeBaseCategoryViewSerializer),
            201: OpenApiResponse(description='Created', response=KnowledgeBaseCategoryViewSerializer),
            # 400: OpenApiResponse(description='Validation failed.'),
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
            200: OpenApiResponse(description='', response=KnowledgeBaseCategoryViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single knowledge base article',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=KnowledgeBaseCategoryViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a knowledge base article',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=KnowledgeBaseCategoryViewSerializer),
            # 201: OpenApiResponse(description='Created', response=OrganizationViewSerializer),
            # # 400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):

    filterset_fields = [
        'name',
        'organization',
        'parent_category',
        'target_user',
        'target_team',
        'is_global',
    ]

    search_fields = [
        'name',
    ]

    model = KnowledgeBaseCategory

    view_description = 'Settings, Knowledge Base Categories'


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ViewSerializer']


        return globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ModelSerializer']

