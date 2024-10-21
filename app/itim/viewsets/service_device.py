from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from itim.serializers.service import Service, ServiceModelSerializer, ServiceViewSerializer

from api.viewsets.common import ModelViewSet


@extend_schema_view(
        list=extend_schema(exclude=True),
        retrieve=extend_schema(exclude=True),
        create=extend_schema(exclude=True),
        update=extend_schema(exclude=True),
        partial_update=extend_schema(exclude=True),
        destroy=extend_schema(exclude=True)
    )
class ViewSet(ModelViewSet):

    model = Service


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ViewSerializer']


        return globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ModelSerializer']


    def get_queryset(self):

        queryset = super().queryset()

        queryset = queryset.filter(device_id=self.kwargs['device_id'])

        self.queryset =  queryset

        return self.queryset
