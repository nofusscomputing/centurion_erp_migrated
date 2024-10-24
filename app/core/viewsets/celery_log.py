from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from core.serializers.celery_log import (
    TaskResult,
    TaskResultModelSerializer,
    TaskResultViewSerializer
)

from api.viewsets.common import ReadOnlyModelViewSet




@extend_schema_view(
    list = extend_schema(
        summary = 'Fetch all Celery Logs',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=TaskResultViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single Celery Log',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=TaskResultViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
)
class ViewSet(ReadOnlyModelViewSet):

    filterset_fields = [
        'periodic_task_name',
        'result',
        'status',
        'task_name',
        'worker',
    ]

    search_fields = [
        'result',
        'task_args',
        'task_name',
        'worker',
    ]

    model = TaskResult

    page_layout: list = [
        {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'task_id',
                        'periodic_task_name',
                        'task_name',
                        'status',
                    ],
                    "right": [
                        'worker',
                        'task_kwargs',
                        'date_created',
                        'date_done',
                        'result',
                    ]
                },
                {
                    "layout": "single",
                    "fields": [
                        "task_args"
                    ]
                }
            ]
        },
    ]

    table_fields: list = [
        'id',
        'task_id',
        'task_name',
        'status',
        'date_done',
        'date_created',
    ]


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()['TaskResultViewSerializer']


        return globals()['TaskResultModelSerializer']
