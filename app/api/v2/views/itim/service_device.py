from django.db.models import Q
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from rest_framework import generics, viewsets
from rest_framework.response import Response

from access.mixin import OrganizationMixin

from api.views.mixin import OrganizationPermissionAPI

from api.v2.serializers.itim.service import Service, ModelSerializer, ViewSerializer

# from itam.models.device import DeviceSoftware

from api.v2.views.metadata import NavigationMetadata


@extend_schema_view(
        list=extend_schema(exclude=True),
        retrieve=extend_schema(exclude=True),
        create=extend_schema(exclude=True),
        update=extend_schema(exclude=True),
        partial_update=extend_schema(exclude=True),
        destroy=extend_schema(exclude=True)
    )
class ViewSet(OrganizationMixin, viewsets.ModelViewSet):

    model = Service

    metadata_class = NavigationMetadata

    permission_classes = [
        OrganizationPermissionAPI
    ]

    # queryset = DeviceSoftware.objects.all()

    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return ViewSerializer


        return ModelSerializer



    def create(self, request, *args, **kwargs):

        # current_device = []

        # if 'uuid' in self.request.POST:

        #     current_device = self.serializer_class.Meta.model.objects.filter(
        #         organization = int(self.request.POST['organization']),
        #         uuid = str(self.request.POST['uuid'])
        #     )

        # if 'serial_number' in self.request.POST and len(current_device) == 0:

        #         current_device = self.serializer_class.Meta.model.objects.filter(
        #             organization = int(self.request.POST['organization']),
        #             serial_number = str(self.request.POST['serial_number'])
        #         )

        # if len(current_device) == 1:

        #     instance = current_device.get()
        #     serializer = self.get_serializer(instance)
        #     return Response(serializer.data)

        return super().create(request, *args, **kwargs)


    def list(self, request, *args, **kwargs):

        return super().list(request, *args, **kwargs)


    def retrieve(self, request, *args, **kwargs):

        return super().retrieve(request, *args, **kwargs)


    def get_queryset(self):

        self.queryset = Service.objects.filter(device_id=self.kwargs['device_id'])

        return self.queryset

    def get_view_name(self):
        if self.detail:
            return "Device Service"
        
        return 'Device Services'
