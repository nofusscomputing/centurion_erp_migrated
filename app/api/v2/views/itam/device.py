from django.db.models import Q
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework import generics, viewsets
from rest_framework.response import Response

from access.mixin import OrganizationMixin

from api.v2.serializers.itam.device import ModelSerializer, ViewSerializer
from api.views.mixin import OrganizationPermissionAPI

from itam.models.device import Device

from api.v2.views.metadata import NavigationMetadata


@extend_schema(tags=['device'])
class ViewSet(OrganizationMixin, viewsets.ModelViewSet):

    metadata_class = NavigationMetadata

    permission_classes = [
        OrganizationPermissionAPI
    ]

    queryset = Device.objects.all()

    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return ViewSerializer


        return ModelSerializer



    @extend_schema(
        summary = 'Create a device',
        description="""Add a new device to the ITAM database.
        If you attempt to create a device and a device with a matching name and uuid or name and serial number
        is found within the database, it will not re-create it. The device will be returned within the message body.
        """,
        tags=['device'],
        methods=["POST"],
        responses = {
            200: OpenApiResponse(description='Device allready exists', response=ViewSerializer),
            201: OpenApiResponse(description='Device created', response=ViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    )
    def create(self, request, *args, **kwargs):

        current_device = []

        if 'uuid' in self.request.POST:

            current_device = self.serializer_class.Meta.model.objects.filter(
                organization = int(self.request.POST['organization']),
                uuid = str(self.request.POST['uuid'])
            )

        if 'serial_number' in self.request.POST and len(current_device) == 0:

                current_device = self.serializer_class.Meta.model.objects.filter(
                    organization = int(self.request.POST['organization']),
                    serial_number = str(self.request.POST['serial_number'])
                )

        if len(current_device) == 1:

            instance = current_device.get()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        return super().create(request, *args, **kwargs)


    @extend_schema( description='Fetch devices that are from the users assigned organization(s)',tags=['device'], methods=["GET"])
    def list(self, request):

        return super().list(request)


    @extend_schema( description='Fetch the selected device', tags=['device'], methods=["GET"])
    def retrieve(self, request, *args, **kwargs):

        return super().retrieve(request, *args, **kwargs)


    def get_queryset(self):

        if self.request.user.is_superuser:

            return self.queryset.filter().order_by('name')

        else:

            return self.queryset.filter(Q(organization__in=self.user_organizations()) | Q(is_global = True)).order_by('name')


    def get_view_name(self):
        if self.detail:
            return "Device"
        
        return 'Devices'
