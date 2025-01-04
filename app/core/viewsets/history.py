from django.db.models import Q

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from api.viewsets.common import ReadOnlyModelViewSet

from core.serializers.history import (
    History,
    HistoryModelSerializer,
    HistoryViewSerializer
)



@extend_schema_view(
    create=extend_schema( exclude = True ),
    destroy = extend_schema( exclude = True ),
    list = extend_schema(
        summary = 'Fetch entire history for a model',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=HistoryViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema( exclude = True ),
    update = extend_schema( exclude = True ),
    partial_update = extend_schema( exclude = True )
)
class ViewSet(ReadOnlyModelViewSet):

    allowed_methods = [
        'GET',
        'OPTIONS'
    ]

    filterset_fields = [
        'item_parent_pk',
        'item_parent_class'
    ]


    model = History


    def get_queryset(self):

        queryset = super().get_queryset()

        self.queryset = queryset.filter(
            Q(item_pk = self.kwargs['model_id'], item_class = self.kwargs['model_class'])
            |
            Q(item_parent_pk = self.kwargs['model_id'], item_parent_class = self.kwargs['model_class'])
        )

        return self.queryset


    def get_serializer_class(self):

        return globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ViewSerializer']


    def get_view_name(self):
        if self.detail:
            return "History"
        
        return 'History'
