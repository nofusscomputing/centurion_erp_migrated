from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from core.serializers.notes import (
    Notes,
    NoteModelSerializer,
    NoteViewSerializer
)

from api.viewsets.common import ModelViewSet



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a note',
        description = '',
        responses = {
            201: OpenApiResponse(description='created', response=NoteViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a note',
        description = ''
    ),
    list = extend_schema(
        summary = 'Fetch all notes',
        description='',
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single note',
        description='',
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a note',
        description = ''
    ),
)
class ViewSet(ModelViewSet):

    filterset_fields = [
        'config_group',
        'device',
    ]

    search_fields = [
        'note',
    ]

    model = Notes


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return ViewSerializer


        return ModelSerializer


    def get_queryset(self):

        queryset = super().get_queryset()

        if 'device_id' in self.kwargs:

            self.queryset = queryset.filter(device_id=self.kwargs['device_id']).order_by('-created')

        elif 'group_id' in self.kwargs:

            self.queryset = queryset.filter(config_group_id=self.kwargs['group_id']).order_by('-created')

        elif 'operating_system_id' in self.kwargs:

            self.queryset = queryset.filter(operatingsystem_id=self.kwargs['operating_system_id']).order_by('-created')

        elif 'service_id' in self.kwargs:

            self.queryset = queryset.filter(service_id=self.kwargs['service_id']).order_by('-created')

        elif 'software_id' in self.kwargs:

            self.queryset = queryset.filter(software_id=self.kwargs['software_id']).order_by('-created')

        else:

            self.queryset = queryset


        return self.queryset


    def get_view_name(self):
        if self.detail:
            return "Note"
        
        return 'Notes'


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ViewSerializer']


        return globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ModelSerializer']
