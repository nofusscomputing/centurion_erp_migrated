from django.db.models import Q
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from rest_framework.fields import empty
from rest_framework import generics, viewsets
from rest_framework.response import Response

from access.mixin import OrganizationMixin

from api.views.mixin import OrganizationPermissionAPI

from api.v2.serializers.itam.device_software import ModelSerializer, ViewSerializer

from itam.models.device import DeviceSoftware

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

    model = DeviceSoftware

    metadata_class = NavigationMetadata

    permission_classes = [
        OrganizationPermissionAPI
    ]

    # queryset = DeviceSoftware.objects.all()

    def get_serializer_class(self):

        kwargs=self.kwargs

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = ViewSerializer

        else:

            self.serializer_class = ModelSerializer

        return self.serializer_class


    def get_serializer_context(self):

        context = super().get_serializer_context()

        context['device_id'] = int(self.kwargs['device_id'])

        return context


    def create(self, request, *args, **kwargs):

        return super().create(request, *args, **kwargs)


    def list(self, request, *args, **kwargs):

        return super().list(request, *args, **kwargs)


    def retrieve(self, request, *args, **kwargs):

        return super().retrieve(request, *args, **kwargs)


    def get_queryset(self):

        self.queryset = DeviceSoftware.objects.filter(device_id=self.kwargs['device_id'])

        return self.queryset

    def get_view_name(self):
        
        return 'Device Software'
